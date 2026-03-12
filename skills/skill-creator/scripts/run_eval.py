#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes Claude to trigger (read the skill)
for a set of queries. Outputs results as JSON.
"""

import argparse
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from scripts.utils import parse_skill_md

# Serialize SKILL.md swaps across parallel workers so they don't corrupt the file.
_skill_swap_lock = threading.Lock()


def find_project_root() -> Path:
    """Find the project root by walking up from cwd looking for .claude/.

    Mimics how Claude Code discovers its project root, so the command file
    we create ends up where claude -p will look for it.
    """
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".claude").is_dir():
            return parent
    return current


def find_plugin_skills_dir(project_root: Path) -> Path | None:
    """Find the plugin cache skills/ dir for the project's active plugin.

    Returns e.g. ~/.claude/plugins/cache/{id}/{name}/{ver}/skills/ so that
    temp eval skills are picked up by Claude Code's init scan as auto-triggered
    skills.  Returns None if no plugin is configured or the cache is absent.
    """
    try:
        settings = json.loads(
            (project_root / ".claude" / "settings.json").read_text(encoding="utf-8")
        )
    except (OSError, ValueError):  # FileNotFoundError ⊆ OSError; JSONDecodeError ⊆ ValueError
        return None

    # First enabled plugin key, e.g. "hugin-v0@hugin-v0"
    plugin_key = next((k for k, v in settings.get("enabledPlugins", {}).items() if v), None)
    if not plugin_key:
        return None

    # split("@", 1) → ["name"] or ["name", "id"]; parts[-1] handles both
    parts = plugin_key.split("@", 1)
    plugin_name, plugin_id = parts[0], parts[-1]

    cache_base = Path.home() / ".claude" / "plugins" / "cache" / plugin_id / plugin_name
    if not cache_base.exists():
        return None

    return next(
        (d / "skills" for d in sorted(cache_base.iterdir(), reverse=True) if (d / "skills").is_dir()),
        None,
    )


def _replace_description_in_frontmatter(content: str, new_description: str) -> str:
    """Return SKILL.md content with the frontmatter description replaced.

    Splits on '---' delimiters to isolate the YAML frontmatter block, then
    uses re.sub to rewrite the 'description:' line in place.
    """
    safe = new_description.replace('"', "'")
    parts = content.split("---", 2)  # ["", frontmatter_body, rest]
    if len(parts) < 3:
        return content
    new_fm = re.sub(r"(?m)^(description:).*$", f'\\1 "{safe}"', parts[1])
    return f"---{new_fm}---{parts[2]}"


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
) -> bool:
    """Run a single query and return whether the skill was triggered.

    Temporarily swaps the description in the real skill's cached SKILL.md, runs
    `claude -p` with the raw query, and checks whether Claude's response includes
    a Skill or Read tool call that references the real skill.  A module-level
    lock serializes concurrent swaps so parallel workers don't corrupt the file.
    """
    project_path = Path(project_root)
    plugin_skills = find_plugin_skills_dir(project_path)
    if plugin_skills:
        skill_md_path = plugin_skills / skill_name / "SKILL.md"
    else:
        skill_md_path = project_path / "skills" / skill_name / "SKILL.md"

    if not skill_md_path.exists():
        return False

    with _skill_swap_lock:
        original_content = skill_md_path.read_text(encoding="utf-8")
        skill_md_path.write_text(
            _replace_description_in_frontmatter(original_content, skill_description),
            encoding="utf-8",
        )
        try:
            return _run_query_subprocess(query, skill_name, timeout, project_root, model)
        finally:
            skill_md_path.write_text(original_content, encoding="utf-8")


def _run_query_subprocess(
    query: str,
    skill_name: str,
    timeout: int,
    project_root: str,
    model: str | None,
) -> bool:
    """Spawn `claude -p` and detect whether skill_name is invoked via Skill tool."""

    cmd = [
        "claude",
        "-p", query,
        "--output-format", "stream-json",
        "--verbose",
        "--include-partial-messages",
    ]
    if model:
        cmd.extend(["--model", model])

    # Remove CLAUDECODE env var to allow nesting claude -p inside a
    # Claude Code session. The guard is for interactive terminal conflicts;
    # programmatic subprocess usage is safe.
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        cwd=project_root,
        env=env,
    )

    triggered = False
    start_time = time.time()
    buffer = ""
    # Track state for stream event detection
    pending_tool_name = None
    accumulated_json = ""

    # Use a reader thread + queue instead of select.select, which
    # doesn't work with pipe file descriptors on Windows (WinError 10038).
    read_queue: queue.Queue = queue.Queue()

    def _pipe_reader(pipe, q):
        try:
            while True:
                chunk = pipe.read(8192)
                if not chunk:
                    break
                q.put(chunk)
        except Exception:
            pass
        finally:
            q.put(None)  # EOF sentinel

    reader_thread = threading.Thread(
        target=_pipe_reader, args=(process.stdout, read_queue), daemon=True
    )
    reader_thread.start()

    try:
        while time.time() - start_time < timeout:
            try:
                chunk = read_queue.get(timeout=1.0)
            except queue.Empty:
                if process.poll() is not None:
                    # Process ended; drain any remaining data
                    while True:
                        try:
                            chunk = read_queue.get_nowait()
                        except queue.Empty:
                            break
                        if chunk is None:
                            break
                        buffer += chunk.decode("utf-8", errors="replace")
                    break
                continue

            if chunk is None:  # EOF sentinel
                break
            buffer += chunk.decode("utf-8", errors="replace")

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue

                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Early detection via stream events
                if event.get("type") == "stream_event":
                    se = event.get("event", {})
                    se_type = se.get("type", "")

                    if se_type == "content_block_start":
                        cb = se.get("content_block", {})
                        if cb.get("type") == "tool_use":
                            tool_name = cb.get("name", "")
                            if tool_name in ("Skill", "Read"):
                                pending_tool_name = tool_name
                                accumulated_json = ""
                            else:
                                return False

                    elif se_type == "content_block_delta" and pending_tool_name:
                        delta = se.get("delta", {})
                        if delta.get("type") == "input_json_delta":
                            accumulated_json += delta.get("partial_json", "")
                            if skill_name in accumulated_json:
                                return True

                    elif se_type in ("content_block_stop", "message_stop"):
                        if pending_tool_name:
                            return skill_name in accumulated_json
                        if se_type == "message_stop":
                            return False

                # Fallback: full assistant message
                elif event.get("type") == "assistant":
                    message = event.get("message", {})
                    for content_item in message.get("content", []):
                        if content_item.get("type") != "tool_use":
                            continue
                        tool_name = content_item.get("name", "")
                        tool_input = content_item.get("input", {})
                        if tool_name == "Skill" and skill_name in tool_input.get("skill", ""):
                            triggered = True
                        elif tool_name == "Read" and skill_name in tool_input.get("file_path", ""):
                            triggered = True
                        return triggered

                elif event.get("type") == "result":
                    return triggered
    finally:
        # Clean up process on any exit path (return, exception, timeout)
        if process.poll() is None:
            process.kill()
            process.wait()

    return triggered


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    results = []

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Model to use for claude -p (default: user's configured model)")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, _ = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
