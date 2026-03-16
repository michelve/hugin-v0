#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Hook Testing Helper
# Tests a hook script with sample JSON input and shows output.
#
# Adapted from anthropics/claude-plugins-official plugin-dev for hugin-v0.
#
# Usage:
#   ./scripts/test-hook.sh <hook-script> <test-input.json>
#   ./scripts/test-hook.sh --create-sample <event-type>
#   ./scripts/test-hook.sh -v -t 30 <hook-script> <test-input.json>
# ---------------------------------------------------------------------------

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# --- Colors ---
if [ -t 1 ]; then
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'
    BOLD='\033[1m'; DIM='\033[2m'; RESET='\033[0m'
else
    RED='' GREEN='' YELLOW='' BOLD='' DIM='' RESET=''
fi

show_usage() {
    cat <<'EOF'
Usage: test-hook.sh [options] <hook-script> <test-input.json>

Options:
  -h, --help            Show this help message
  -v, --verbose         Show detailed execution information
  -t, --timeout N       Set timeout in seconds (default: 60)
  --create-sample TYPE  Print sample JSON for an event type and exit

Supported event types:
  SessionStart, PreToolUse, PostToolUse, UserPromptSubmit, Stop

Examples:
  # Generate sample input
  ./scripts/test-hook.sh --create-sample PreToolUse > /tmp/test.json

  # Test a hook
  ./scripts/test-hook.sh scripts/setup-env-check.py /tmp/test.json

  # Verbose with timeout
  ./scripts/test-hook.sh -v -t 30 scripts/commitlint-enforcer.py /tmp/test.json
EOF
    exit 0
}

create_sample() {
    local event_type="$1"
    case "$event_type" in
        PreToolUse)
            cat <<'SAMPLE'
{
  "session_id": "test-session-001",
  "transcript_path": "/tmp/transcript.txt",
  "cwd": "/tmp/test-project",
  "permission_mode": "ask",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "git commit -m 'feat: add new feature'"
  }
}
SAMPLE
            ;;
        PostToolUse)
            cat <<'SAMPLE'
{
  "session_id": "test-session-001",
  "transcript_path": "/tmp/transcript.txt",
  "cwd": "/tmp/test-project",
  "permission_mode": "ask",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/tmp/test-project/src/App.tsx",
    "content": "export function App() { return <div>Hello</div>; }"
  },
  "tool_result": "File written successfully"
}
SAMPLE
            ;;
        UserPromptSubmit)
            cat <<'SAMPLE'
{
  "session_id": "test-session-001",
  "transcript_path": "/tmp/transcript.txt",
  "cwd": "/tmp/test-project",
  "permission_mode": "ask",
  "hook_event_name": "UserPromptSubmit",
  "user_prompt": "implement task #0005 add user dashboard"
}
SAMPLE
            ;;
        Stop)
            cat <<'SAMPLE'
{
  "session_id": "test-session-001",
  "transcript_path": "/tmp/transcript.txt",
  "cwd": "/tmp/test-project",
  "permission_mode": "ask",
  "hook_event_name": "Stop",
  "reason": "Task appears complete"
}
SAMPLE
            ;;
        SessionStart)
            cat <<'SAMPLE'
{
  "session_id": "test-session-001",
  "transcript_path": "/tmp/transcript.txt",
  "cwd": "/tmp/test-project",
  "permission_mode": "ask",
  "hook_event_name": "SessionStart"
}
SAMPLE
            ;;
        *)
            echo "Unknown event type: $event_type" >&2
            echo "Valid types: SessionStart, PreToolUse, PostToolUse, UserPromptSubmit, Stop" >&2
            exit 1
            ;;
    esac
}

# --- Parse arguments ---
VERBOSE=false
TIMEOUT=60

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help) show_usage ;;
        -v|--verbose) VERBOSE=true; shift ;;
        -t|--timeout) TIMEOUT="$2"; shift 2 ;;
        --create-sample)
            create_sample "$2"
            exit 0
            ;;
        *) break ;;
    esac
done

if [ $# -ne 2 ]; then
    echo -e "${RED}Error: expected <hook-script> <test-input.json>${RESET}" >&2
    echo ""
    show_usage
fi

HOOK_SCRIPT="$1"
TEST_INPUT="$2"

# --- Validate inputs ---
if [ ! -f "$HOOK_SCRIPT" ]; then
    echo -e "${RED}❌ Hook script not found: $HOOK_SCRIPT${RESET}" >&2
    exit 1
fi

if [ ! -f "$TEST_INPUT" ]; then
    echo -e "${RED}❌ Test input not found: $TEST_INPUT${RESET}" >&2
    exit 1
fi

# Validate test input is valid JSON
if command -v jq &>/dev/null; then
    if ! jq empty "$TEST_INPUT" 2>/dev/null; then
        echo -e "${RED}❌ Test input is not valid JSON${RESET}" >&2
        exit 1
    fi
elif command -v python3 &>/dev/null; then
    if ! python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$TEST_INPUT" 2>/dev/null; then
        echo -e "${RED}❌ Test input is not valid JSON${RESET}" >&2
        exit 1
    fi
fi

# Detect hook type (Python or shell)
if [[ "$HOOK_SCRIPT" == *.py ]]; then
    RUNNER="python3"
elif [[ "$HOOK_SCRIPT" == *.sh ]]; then
    RUNNER="bash"
else
    RUNNER="bash"
fi

echo -e "${BOLD}🧪 Testing hook: ${HOOK_SCRIPT}${RESET}"
echo -e "📥 Input: ${TEST_INPUT}"
echo ""

if [ "$VERBOSE" = true ]; then
    echo -e "${DIM}Input JSON:${RESET}"
    if command -v jq &>/dev/null; then
        jq . "$TEST_INPUT"
    else
        cat "$TEST_INPUT"
    fi
    echo ""
fi

# --- Set up environment ---
export CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-/tmp/test-project}"
export CLAUDE_PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$REPO_ROOT}"

if [ "$VERBOSE" = true ]; then
    echo -e "${DIM}Environment:${RESET}"
    echo "  CLAUDE_PROJECT_DIR=$CLAUDE_PROJECT_DIR"
    echo "  CLAUDE_PLUGIN_ROOT=$CLAUDE_PLUGIN_ROOT"
    echo ""
fi

# --- Run the hook ---
echo -e "▶️  Running hook (timeout: ${TIMEOUT}s)..."
echo ""

start_time=$(date +%s)

set +e
if command -v gtimeout &>/dev/null; then
    TIMEOUT_CMD="gtimeout"
elif command -v timeout &>/dev/null; then
    TIMEOUT_CMD="timeout"
else
    TIMEOUT_CMD=""
fi

if [ -n "$TIMEOUT_CMD" ]; then
    output=$($TIMEOUT_CMD "$TIMEOUT" $RUNNER "$HOOK_SCRIPT" < "$TEST_INPUT" 2>&1)
else
    output=$($RUNNER "$HOOK_SCRIPT" < "$TEST_INPUT" 2>&1)
fi
exit_code=$?
set -e

end_time=$(date +%s)
duration=$((end_time - start_time))

# --- Analyze results ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BOLD}Results:${RESET}"
echo ""
echo "Exit Code: $exit_code"
echo "Duration:  ${duration}s"
echo ""

case $exit_code in
    0)  echo -e "${GREEN}✅ Hook approved/succeeded${RESET}" ;;
    2)  echo -e "${YELLOW}🚫 Hook blocked/denied${RESET}" ;;
    124) echo -e "${RED}⏱️  Hook timed out after ${TIMEOUT}s${RESET}" ;;
    *)  echo -e "${RED}⚠️  Hook returned unexpected exit code: $exit_code${RESET}" ;;
esac

echo ""
echo -e "${BOLD}Output:${RESET}"
if [ -n "$output" ]; then
    echo "$output"
    echo ""

    # Try to parse as JSON
    if command -v jq &>/dev/null && echo "$output" | jq empty 2>/dev/null; then
        echo -e "${DIM}(valid JSON output)${RESET}"
    fi
else
    echo "(no output)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $exit_code -eq 0 ] || [ $exit_code -eq 2 ]; then
    echo -e "${GREEN}✅ Test completed successfully${RESET}"
    exit 0
else
    echo -e "${RED}❌ Test failed${RESET}"
    exit 1
fi
