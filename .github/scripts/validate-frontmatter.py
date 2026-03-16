#!/usr/bin/env python3
"""
Validate YAML frontmatter in agent, skill, command, and output-style .md files.

Usage:
    python validate-frontmatter.py                     # scan repo root
    python validate-frontmatter.py /path/to/dir        # scan specific directory
    python validate-frontmatter.py file1.md file2.md   # validate specific files
    python validate-frontmatter.py --fix               # scan + auto-fix missing scaffolds
    python validate-frontmatter.py --fix file.md       # fix specific files

The --fix flag generates missing scaffolds (evals/, skills-rules.json) for skills.
Exit code 0 when all files pass, 1 when any errors are found.
"""

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# YAML parsing — stdlib only (no PyYAML dependency on CI)
# ---------------------------------------------------------------------------

# Characters that need quoting in YAML values when unquoted
_YAML_SPECIAL = re.compile(r'[{}\[\]*&#!|>%@`]')
_FRONTMATTER_RE = re.compile(r'^---[ \t]*\n(.*?)^---[ \t]*\n?', re.MULTILINE | re.DOTALL)


def _quote_special_values(text: str) -> str:
    """Pre-process frontmatter to quote values with special YAML chars."""
    lines = text.split('\n')
    result: list[str] = []
    for line in lines:
        m = re.match(r'^([a-zA-Z_-]+):\s+(.+)$', line)
        if m:
            key, value = m.group(1), m.group(2)
            if not ((value.startswith('"') and value.endswith('"')) or
                    (value.startswith("'") and value.endswith("'"))):
                if _YAML_SPECIAL.search(value):
                    escaped = value.replace('\\', '\\\\').replace('"', '\\"')
                    result.append(f'{key}: "{escaped}"')
                    continue
        result.append(line)
    return '\n'.join(result)


def _parse_yaml_simple(text: str) -> dict:
    """Minimal YAML parser for flat frontmatter (handles scalars and lists)."""
    result: dict = {}
    current_key: str | None = None
    current_list: list | None = None

    for line in text.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        # List item under current key
        if stripped.startswith('- ') and current_key is not None and current_list is not None:
            current_list.append(stripped[2:].strip())
            continue

        # Top-level key: value
        m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_-]*):\s*(.*)', line)
        if m:
            # Save previous list if any
            if current_key is not None and current_list is not None:
                result[current_key] = current_list

            key = m.group(1)
            value = m.group(2).strip()

            if value == '':
                # Could be a list or block scalar starting on next line
                current_key = key
                current_list = []
                continue

            # Unquote strings
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]

            # YAML booleans
            if value.lower() in ('true', 'yes'):
                result[key] = True
            elif value.lower() in ('false', 'no'):
                result[key] = False
            else:
                result[key] = value

            current_key = key
            current_list = None
            continue

        # Indented key under a mapping (e.g. metadata sub-keys) — skip
        if line.startswith('    ') or line.startswith('\t'):
            continue

    # Save trailing list
    if current_key is not None and current_list is not None and current_list:
        result[current_key] = current_list

    return result


def parse_frontmatter(content: str) -> tuple[dict | None, str | None]:
    """Return (frontmatter_dict, error_message)."""
    m = _FRONTMATTER_RE.search(content)
    if not m:
        return None, 'No frontmatter found'

    raw = _quote_special_values(m.group(1))
    try:
        parsed = _parse_yaml_simple(raw)
    except Exception as e:
        return None, f'YAML parse failed: {e}'

    if not isinstance(parsed, dict):
        return None, f'Frontmatter is not a mapping (got {type(parsed).__name__})'
    return parsed, None


# ---------------------------------------------------------------------------
# Allowed properties per file type
# ---------------------------------------------------------------------------

# Skills — official Claude Code fields + Cowork extras
SKILL_ALLOWED = {
    # Official Claude Code fields (10)
    'name', 'description', 'argument-hint', 'disable-model-invocation',
    'user-invocable', 'allowed-tools', 'model', 'context', 'agent', 'hooks',
    # Cowork platform extras
    'version', 'license', 'metadata', 'compatibility',
}

# Agents/Subagents — official Claude Code fields + color (used by all agents)
AGENT_ALLOWED = {
    'name', 'description', 'tools', 'disallowedTools', 'model',
    'permissionMode', 'maxTurns', 'skills', 'mcpServers', 'hooks',
    'memory', 'background', 'isolation',
    # Plugin UI extension
    'color',
}

# Commands — same frontmatter as skills per official docs
COMMAND_ALLOWED = SKILL_ALLOWED

# Output styles — plugin-custom
OUTPUT_STYLE_ALLOWED = {
    'name', 'description', 'keep-coding-instructions',
}

# ---------------------------------------------------------------------------
# Validation per file type
# ---------------------------------------------------------------------------

def _validate_skill(fm: dict) -> list[tuple[str, str]]:
    """Return list of (level, message) issues."""
    issues: list[tuple[str, str]] = []

    # Allowed keys
    unexpected = set(fm.keys()) - SKILL_ALLOWED
    for k in sorted(unexpected):
        issues.append(('error', f'Unexpected key "{k}". Allowed: {", ".join(sorted(SKILL_ALLOWED))}'))

    # Required: description (name defaults to directory name per docs)
    if 'description' not in fm:
        issues.append(('error', 'Missing required "description" field'))

    # Name validation (if present)
    name = fm.get('name')
    if name is not None:
        if not isinstance(name, str):
            issues.append(('error', f'name must be a string, got {type(name).__name__}'))
        else:
            name = name.strip()
            if name:
                if not re.match(r'^[a-z0-9-]+$', name):
                    issues.append(('error', f'name "{name}" must be kebab-case (lowercase, digits, hyphens)'))
                if name.startswith('-') or name.endswith('-') or '--' in name:
                    issues.append(('error', f'name "{name}" cannot start/end with hyphen or have consecutive hyphens'))
                if len(name) > 64:
                    issues.append(('error', f'name is too long ({len(name)} chars, max 64)'))

    # Description validation
    desc = fm.get('description')
    if desc is not None and isinstance(desc, str):
        if len(desc) > 1024:
            issues.append(('error', f'description is too long ({len(desc)} chars, max 1024)'))

    # Compatibility validation
    compat = fm.get('compatibility')
    if compat is not None:
        if not isinstance(compat, str):
            issues.append(('error', f'compatibility must be a string, got {type(compat).__name__}'))
        elif len(compat) > 500:
            issues.append(('error', f'compatibility is too long ({len(compat)} chars, max 500)'))

    return issues


def _validate_agent(fm: dict) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []

    unexpected = set(fm.keys()) - AGENT_ALLOWED
    for k in sorted(unexpected):
        issues.append(('error', f'Unexpected key "{k}". Allowed: {", ".join(sorted(AGENT_ALLOWED))}'))

    if 'name' not in fm or not fm.get('name'):
        issues.append(('error', 'Missing required "name" field'))
    if 'description' not in fm or not fm.get('description'):
        issues.append(('error', 'Missing required "description" field'))

    return issues


def _validate_command(fm: dict) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []

    unexpected = set(fm.keys()) - COMMAND_ALLOWED
    for k in sorted(unexpected):
        issues.append(('error', f'Unexpected key "{k}". Allowed: {", ".join(sorted(COMMAND_ALLOWED))}'))

    if 'description' not in fm or not fm.get('description'):
        issues.append(('error', 'Missing required "description" field'))

    return issues


def _validate_output_style(fm: dict) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []

    unexpected = set(fm.keys()) - OUTPUT_STYLE_ALLOWED
    for k in sorted(unexpected):
        issues.append(('error', f'Unexpected key "{k}". Allowed: {", ".join(sorted(OUTPUT_STYLE_ALLOWED))}'))

    if 'name' not in fm or not fm.get('name'):
        issues.append(('error', 'Missing required "name" field'))
    if 'description' not in fm or not fm.get('description'):
        issues.append(('error', 'Missing required "description" field'))

    return issues


# ---------------------------------------------------------------------------
# Quality checks (warnings) — skill files only
# ---------------------------------------------------------------------------

_TOC_HEADING_RE = re.compile(
    r'^#{1,3}\s+(table of contents|contents|toc)\b',
    re.IGNORECASE,
)
_TOC_LINK_RE = re.compile(r'^\s*-\s+\[.+\]\(#')


def _quality_checks_skill(
    fm: dict, filepath: Path, content: str, base: Path,
) -> list[tuple[str, str]]:
    """Return warnings for skill quality rules from the spec."""
    issues: list[tuple[str, str]] = []
    lines = content.splitlines()
    line_count = len(lines)

    # --- 500-line hard limit ---
    if line_count > 500:
        issues.append((
            'error',
            f'SKILL.md is {line_count} lines (hard limit: 500). '
            'Extract reference material to supporting files.',
        ))

    # --- TOC required for files > 100 lines ---
    if line_count > 100:
        has_toc = False
        for line in lines:
            if _TOC_HEADING_RE.match(line):
                has_toc = True
                break
        if not has_toc:
            # Heuristic: 3+ consecutive anchor-links suggest an implicit TOC
            consecutive_links = 0
            for line in lines:
                if _TOC_LINK_RE.match(line):
                    consecutive_links += 1
                    if consecutive_links >= 3:
                        has_toc = True
                        break
                else:
                    consecutive_links = 0
        if not has_toc:
            issues.append((
                'warn',
                f'SKILL.md is {line_count} lines but has no table of contents '
                '(recommended for files > 100 lines).',
            ))

    # --- Name vs directory name consistency ---
    name = fm.get('name')
    if name and isinstance(name, str):
        dir_name = filepath.parent.name
        if name.strip() != dir_name:
            issues.append((
                'warn',
                f'name "{name}" does not match directory name "{dir_name}".',
            ))

    # --- Description quality ---
    desc = fm.get('description')
    if desc and isinstance(desc, str):
        if len(desc) < 20:
            issues.append((
                'warn',
                f'description is very short ({len(desc)} chars). '
                'Include what the skill does AND when to use it.',
            ))

    # --- context field value validation ---
    ctx = fm.get('context')
    if ctx is not None and isinstance(ctx, str) and ctx != 'fork':
        issues.append((
            'error',
            f'context value "{ctx}" is invalid. Only "fork" is supported.',
        ))

    # --- evals/ presence ---
    evals_dir = filepath.parent / 'evals'
    if not evals_dir.is_dir():
        issues.append((
            'warn',
            'No evals/ directory. Consider adding evaluations '
            '(evals.json + trigger-evals.json).',
        ))
    else:
        evals_json = evals_dir / 'evals.json'
        if not evals_json.is_file():
            issues.append((
                'warn', 'evals/ directory exists but evals.json is missing.',
            ))
        else:
            issues.extend(_validate_evals_schema(evals_json, filepath))

        trigger_evals = evals_dir / 'trigger-evals.json'
        if not trigger_evals.is_file():
            issues.append((
                'warn',
                'evals/ directory exists but trigger-evals.json is missing.',
            ))
        else:
            issues.extend(_validate_trigger_evals_schema(trigger_evals))

    # --- skills-rules.json ---
    rules_file = filepath.parent / 'skills-rules.json'
    if not rules_file.is_file():
        issues.append((
            'warn',
            'No skills-rules.json found. Skill may not have trigger patterns.',
        ))
    else:
        issues.extend(_validate_skill_rules(rules_file, filepath))

    return issues


def _validate_evals_schema(
    evals_path: Path, skill_path: Path,
) -> list[tuple[str, str]]:
    """Validate evals.json structure."""
    issues: list[tuple[str, str]] = []
    try:
        data = json.loads(evals_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        issues.append(('error', f'evals.json: invalid JSON — {exc}'))
        return issues
    except OSError as exc:
        issues.append(('error', f'evals.json: cannot read — {exc}'))
        return issues

    if not isinstance(data, dict):
        issues.append(('error', 'evals.json: root must be an object'))
        return issues

    # skill_name check
    skill_name = data.get('skill_name')
    if not skill_name:
        issues.append(('error', 'evals.json: missing "skill_name" field'))
    elif isinstance(skill_name, str):
        dir_name = skill_path.parent.name
        if skill_name != dir_name:
            issues.append((
                'warn',
                f'evals.json: skill_name "{skill_name}" does not match '
                f'directory name "{dir_name}".',
            ))

    # evals array
    evals = data.get('evals')
    if evals is None:
        issues.append(('error', 'evals.json: missing "evals" array'))
    elif not isinstance(evals, list):
        issues.append(('error', 'evals.json: "evals" must be an array'))
    elif len(evals) == 0:
        issues.append(('warn', 'evals.json: "evals" array is empty'))
    else:
        for i, ev in enumerate(evals):
            if not isinstance(ev, dict):
                issues.append((
                    'error', f'evals.json: eval[{i}] must be an object',
                ))
                continue
            if 'id' not in ev:
                issues.append(('error', f'evals.json: eval[{i}] missing "id"'))
            if 'prompt' not in ev or not ev.get('prompt'):
                issues.append((
                    'error', f'evals.json: eval[{i}] missing "prompt"',
                ))
            expectations = ev.get('expectations')
            if not expectations:
                issues.append((
                    'warn',
                    f'evals.json: eval[{i}] has no expectations.',
                ))
            elif not isinstance(expectations, list):
                issues.append((
                    'error',
                    f'evals.json: eval[{i}] expectations must be an array',
                ))

    return issues


def _validate_trigger_evals_schema(
    path: Path,
) -> list[tuple[str, str]]:
    """Validate trigger-evals.json structure."""
    issues: list[tuple[str, str]] = []
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        issues.append(('error', f'trigger-evals.json: invalid JSON — {exc}'))
        return issues
    except OSError as exc:
        issues.append(('error', f'trigger-evals.json: cannot read — {exc}'))
        return issues

    if not isinstance(data, list):
        issues.append(('error', 'trigger-evals.json: root must be an array'))
        return issues

    if len(data) == 0:
        issues.append(('warn', 'trigger-evals.json: array is empty'))
        return issues

    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            issues.append((
                'error', f'trigger-evals.json: entry[{i}] must be an object',
            ))
            continue
        if 'query' not in entry or not entry.get('query'):
            issues.append((
                'error', f'trigger-evals.json: entry[{i}] missing "query"',
            ))
        if 'should_trigger' not in entry:
            issues.append((
                'error',
                f'trigger-evals.json: entry[{i}] missing "should_trigger"',
            ))
        elif not isinstance(entry['should_trigger'], bool):
            issues.append((
                'error',
                f'trigger-evals.json: entry[{i}] "should_trigger" must be boolean',
            ))

    return issues


def _validate_skill_rules(
    rules_path: Path, skill_path: Path,
) -> list[tuple[str, str]]:
    """Validate skills-rules.json basic structure."""
    issues: list[tuple[str, str]] = []
    try:
        data = json.loads(rules_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        issues.append(('error', f'skills-rules.json: invalid JSON — {exc}'))
        return issues
    except OSError as exc:
        issues.append(('error', f'skills-rules.json: cannot read — {exc}'))
        return issues

    if not isinstance(data, dict):
        issues.append(('error', 'skills-rules.json: root must be an object'))
        return issues

    if 'name' not in data:
        issues.append(('warn', 'skills-rules.json: missing "name" field'))
    elif isinstance(data['name'], str):
        dir_name = skill_path.parent.name
        if data['name'] != dir_name:
            issues.append((
                'warn',
                f'skills-rules.json: name "{data["name"]}" does not match '
                f'directory name "{dir_name}".',
            ))

    if 'description' not in data:
        issues.append(('warn', 'skills-rules.json: missing "description" field'))

    return issues


# ---------------------------------------------------------------------------
# Hooks.json validation
# ---------------------------------------------------------------------------

VALID_HOOK_EVENTS = {
    'PreToolUse', 'PostToolUse', 'PostToolUseFailure',
    'UserPromptSubmit', 'Stop', 'Notification',
    'SubagentStart', 'SubagentStop',
    'SessionStart', 'SessionStop',
    'PreCompact', 'PostCompact',
    'TaskStart', 'TaskCompleted',
}

VALID_HOOK_TYPES = {'command', 'prompt', 'agent', 'http'}


def _validate_hooks_json(base: Path) -> list[tuple[str, str]]:
    """Validate hooks/hooks.json structure and event types."""
    issues: list[tuple[str, str]] = []
    hooks_path = base / 'hooks' / 'hooks.json'
    if not hooks_path.is_file():
        return issues

    try:
        data = json.loads(hooks_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        issues.append(('error', f'hooks.json: invalid JSON — {exc}'))
        return issues
    except OSError as exc:
        issues.append(('error', f'hooks.json: cannot read — {exc}'))
        return issues

    if not isinstance(data, dict):
        issues.append(('error', 'hooks.json: root must be an object'))
        return issues

    hooks_obj = data.get('hooks', data)
    if not isinstance(hooks_obj, dict):
        issues.append(('error', 'hooks.json: "hooks" must be an object'))
        return issues

    for event_name, handlers in hooks_obj.items():
        if event_name not in VALID_HOOK_EVENTS:
            issues.append((
                'warn',
                f'hooks.json: unknown event type "{event_name}". '
                f'Known types: {", ".join(sorted(VALID_HOOK_EVENTS))}',
            ))

        if not isinstance(handlers, list):
            issues.append((
                'error',
                f'hooks.json: "{event_name}" handlers must be an array',
            ))
            continue

        for i, handler in enumerate(handlers):
            if not isinstance(handler, dict):
                issues.append((
                    'error',
                    f'hooks.json: {event_name}[{i}] must be an object',
                ))
                continue

            hook_list = handler.get('hooks', [])
            if not isinstance(hook_list, list) or not hook_list:
                issues.append((
                    'error',
                    f'hooks.json: {event_name}[{i}] must have '
                    f'non-empty "hooks" array',
                ))
                continue

            for j, hook in enumerate(hook_list):
                if not isinstance(hook, dict):
                    issues.append((
                        'error',
                        f'hooks.json: {event_name}[{i}].hooks[{j}] '
                        f'must be an object',
                    ))
                    continue

                hook_type = hook.get('type')
                if not hook_type:
                    issues.append((
                        'error',
                        f'hooks.json: {event_name}[{i}].hooks[{j}] '
                        f'missing "type" field',
                    ))
                elif hook_type not in VALID_HOOK_TYPES:
                    issues.append((
                        'error',
                        f'hooks.json: {event_name}[{i}].hooks[{j}] '
                        f'unknown type "{hook_type}". '
                        f'Valid: {", ".join(sorted(VALID_HOOK_TYPES))}',
                    ))

                if hook_type == 'command' and 'command' not in hook:
                    issues.append((
                        'error',
                        f'hooks.json: {event_name}[{i}].hooks[{j}] '
                        f'type "command" requires "command" field',
                    ))

                async_val = hook.get('async')
                if async_val is not None and not isinstance(async_val, bool):
                    issues.append((
                        'warn',
                        f'hooks.json: {event_name}[{i}].hooks[{j}] '
                        f'"async" should be a boolean',
                    ))

                # Timeout range warning
                timeout_val = hook.get('timeout')
                if timeout_val is not None:
                    if isinstance(timeout_val, (int, float)):
                        if timeout_val > 600:
                            issues.append((
                                'warn',
                                f'hooks.json: {event_name}[{i}].hooks[{j}] '
                                f'timeout {timeout_val}s is very high (>600s)',
                            ))
                        elif timeout_val < 5:
                            issues.append((
                                'warn',
                                f'hooks.json: {event_name}[{i}].hooks[{j}] '
                                f'timeout {timeout_val}s is very low (<5s)',
                            ))

                # CLAUDE_PLUGIN_ROOT portability check
                cmd = hook.get('command', '')
                if isinstance(cmd, str) and cmd:
                    if ('/home/' in cmd or '/Users/' in cmd
                            or '/opt/' in cmd or '/usr/local/' in cmd):
                        if '${CLAUDE_PLUGIN_ROOT}' not in cmd:
                            issues.append((
                                'warn',
                                f'hooks.json: {event_name}[{i}].hooks[{j}] '
                                f'command has hardcoded absolute path. '
                                f'Use ${{CLAUDE_PLUGIN_ROOT}} for portability',
                            ))

    return issues


def _validate_settings_agent_ref(base: Path) -> list[tuple[str, str]]:
    """Validate settings.json agent reference points to an existing agent."""
    issues: list[tuple[str, str]] = []
    settings_path = base / 'settings.json'
    if not settings_path.is_file():
        return issues

    try:
        data = json.loads(settings_path.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError):
        return issues

    agent_name = data.get('agent')
    if not agent_name or not isinstance(agent_name, str):
        return issues

    agents_dir = base / 'agents'
    if not agents_dir.is_dir():
        issues.append((
            'warn',
            f'settings.json references agent "{agent_name}" '
            'but agents/ directory does not exist.',
        ))
        return issues

    agent_file = agents_dir / f'{agent_name}.md'
    if not agent_file.is_file():
        issues.append((
            'warn',
            f'settings.json references agent "{agent_name}" '
            f'but agents/{agent_name}.md does not exist.',
        ))

    return issues


# ---------------------------------------------------------------------------
# File type detection
# ---------------------------------------------------------------------------

def detect_file_type(path: Path) -> str | None:
    """Return 'agent', 'skill', 'command', 'output-style', or None."""
    parts = path.as_posix()
    # Don't match files nested inside a skill's own subdirectories
    in_skill_content = bool(re.search(r'/skills/[^/]+/', parts))

    if '/agents/' in parts and not in_skill_content:
        return 'agent'
    if '/skills/' in parts and path.name == 'SKILL.md':
        return 'skill'
    if '/commands/' in parts and not in_skill_content:
        return 'command'
    if '/output-styles/' in parts:
        return 'output-style'
    return None


_VALIDATORS = {
    'agent': _validate_agent,
    'skill': _validate_skill,
    'command': _validate_command,
    'output-style': _validate_output_style,
}

# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def find_files(base: Path) -> list[tuple[Path, str]]:
    """Walk base and return (path, type) for validatable .md files."""
    results: list[tuple[Path, str]] = []
    for p in sorted(base.rglob('*.md')):
        ft = detect_file_type(p)
        if ft:
            results.append((p, ft))
    return results


# ---------------------------------------------------------------------------
# Auto-fix: scaffold missing files for skills
# ---------------------------------------------------------------------------

def _fix_skill(filepath: Path, fm: dict) -> int:
    """Generate missing scaffold files for a skill. Returns count of fixes."""
    fixes = 0
    skill_dir = filepath.parent
    dir_name = skill_dir.name
    desc = fm.get('description', '')
    if not isinstance(desc, str):
        desc = ''

    # --- Generate evals/ directory + skeleton files ---
    evals_dir = skill_dir / 'evals'
    evals_json = evals_dir / 'evals.json'
    trigger_json = evals_dir / 'trigger-evals.json'

    if not evals_dir.is_dir():
        evals_dir.mkdir(parents=True, exist_ok=True)
        print(f'  FIXED: created evals/ directory')
        fixes += 1

    if not evals_json.is_file():
        skeleton = {
            'skill_name': dir_name,
            'evals': [
                {
                    'id': 1,
                    'prompt': 'TODO: Add a realistic user prompt for this skill',
                    'expected_output': 'TODO: Describe what good output looks like',
                    'files': [],
                    'expectations': [
                        'TODO: Add specific, verifiable expectations',
                    ],
                },
            ],
        }
        evals_json.write_text(
            json.dumps(skeleton, indent=2) + '\n', encoding='utf-8',
        )
        print(f'  FIXED: created evals/evals.json skeleton')
        fixes += 1

    if not trigger_json.is_file():
        skeleton = [
            {
                'query': 'TODO: Add a query that SHOULD trigger this skill',
                'should_trigger': True,
            },
            {
                'query': 'TODO: Add a query that should NOT trigger this skill',
                'should_trigger': False,
            },
        ]
        trigger_json.write_text(
            json.dumps(skeleton, indent=2) + '\n', encoding='utf-8',
        )
        print(f'  FIXED: created evals/trigger-evals.json skeleton')
        fixes += 1

    # --- Generate skills-rules.json ---
    rules_file = skill_dir / 'skills-rules.json'
    if not rules_file.is_file():
        skeleton = {
            'name': dir_name,
            'description': desc if desc else f'TODO: Add trigger description for {dir_name}',
        }
        rules_file.write_text(
            json.dumps(skeleton, indent=2) + '\n', encoding='utf-8',
        )
        print(f'  FIXED: created skills-rules.json skeleton')
        fixes += 1

    return fixes


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    args = sys.argv[1:]

    fix_mode = '--fix' in args
    if fix_mode:
        args = [a for a in args if a != '--fix']

    if args and all(a.endswith('.md') for a in args):
        base = Path.cwd()
        files = []
        for a in args:
            p = Path(a).resolve()
            ft = detect_file_type(p)
            if ft:
                files.append((p, ft))
    else:
        base = Path(args[0]).resolve() if args else Path.cwd()
        files = find_files(base)

    total_errors = 0
    total_warnings = 0
    total_fixes = 0

    print(f'Validating {len(files)} frontmatter files...\n')

    for filepath, filetype in files:
        try:
            rel = filepath.relative_to(base)
        except ValueError:
            rel = filepath

        content = filepath.read_text(encoding='utf-8')
        fm, parse_err = parse_frontmatter(content)

        issues: list[tuple[str, str]] = []
        if parse_err:
            issues.append(('error', parse_err))
        else:
            validator = _VALIDATORS[filetype]
            issues.extend(validator(fm))

            # Quality checks for skills (warnings + 500-line error)
            if filetype == 'skill':
                issues.extend(
                    _quality_checks_skill(fm, filepath, content, base),
                )

        if issues:
            print(f'{rel} ({filetype})')
            for level, msg in issues:
                prefix = '  ERROR' if level == 'error' else '  WARN '
                print(f'{prefix}: {msg}')
                if level == 'error':
                    total_errors += 1
                else:
                    total_warnings += 1

            # Auto-fix for skills when --fix is active
            if fix_mode and filetype == 'skill' and fm is not None:
                total_fixes += _fix_skill(filepath, fm)

            print()

    # hooks.json structure check
    hooks_issues = _validate_hooks_json(base)
    if hooks_issues:
        print('hooks/hooks.json')
        for level, msg in hooks_issues:
            prefix = '  ERROR' if level == 'error' else '  WARN '
            print(f'{prefix}: {msg}')
            if level == 'error':
                total_errors += 1
            else:
                total_warnings += 1
        print()

    # settings.json agent reference check
    settings_issues = _validate_settings_agent_ref(base)
    if settings_issues:
        print('settings.json')
        for level, msg in settings_issues:
            prefix = '  ERROR' if level == 'error' else '  WARN '
            print(f'{prefix}: {msg}')
            if level == 'error':
                total_errors += 1
            else:
                total_warnings += 1
        print()

    # In fix mode, also scaffold skills that had no issues
    if fix_mode:
        for filepath, filetype in files:
            if filetype != 'skill':
                continue
            content = filepath.read_text(encoding='utf-8')
            fm, parse_err = parse_frontmatter(content)
            if parse_err or fm is None:
                continue
            skill_dir = filepath.parent
            needs_fix = (
                not (skill_dir / 'evals').is_dir()
                or not (skill_dir / 'evals' / 'evals.json').is_file()
                or not (skill_dir / 'evals' / 'trigger-evals.json').is_file()
                or not (skill_dir / 'skills-rules.json').is_file()
            )
            if needs_fix:
                try:
                    rel = filepath.relative_to(base)
                except ValueError:
                    rel = filepath
                print(f'{rel} ({filetype})')
                total_fixes += _fix_skill(filepath, fm)
                print()

    print('---')
    summary = f'Validated {len(files)} files: {total_errors} errors, {total_warnings} warnings'
    if fix_mode:
        summary += f', {total_fixes} fixes applied'
    print(summary)

    return 1 if total_errors > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
