#!/usr/bin/env node
/**
 * Cross-platform hook runner.
 * On Windows: uses `py` launcher (C:\WINDOWS\py.exe) to bypass the
 * App Execution Alias stub that intercepts `python`/`python3` in some
 * subprocess environments.
 * On macOS/Linux: uses `python3` (standard).
 *
 * Usage: node .claude/hooks/run-hook.js <hook-filename.py>
 * Stdin is forwarded so Claude Code's JSON payload reaches the hook.
 */
const { spawnSync } = require("child_process");
const path = require("path");

const script = process.argv[2];
if (!script) {
    process.stderr.write("run-hook.js: no hook script specified\n");
    process.exit(1);
}

const python = process.platform === "win32" ? "py" : "python3";
const hookPath = path.resolve(__dirname, script);

const result = spawnSync(python, [hookPath], {
    stdio: "inherit",
    shell: false,
});

process.exit(result.status ?? 1);
