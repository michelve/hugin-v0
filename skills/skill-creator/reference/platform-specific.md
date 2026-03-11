# Platform-Specific Instructions

## Claude.ai-Specific Instructions

When creating a Claude.ai skill (Claude.ai / Projects), pay attention to the following:

1. Skills are called "Project instructions". The user creates a project, opens Edit → Project instructions, and pastes/writes their instructions
2. Skills can include attached files (knowledge). These are injected into the system prompt
3. Claude.ai instructions support _all features described in this skill_ (dynamic context, cross-references, etc.), EXCEPT: the `!`command`` syntax for running shell commands. This is only available in Claude Code
4. There's currently no standardized YAML frontmatter convention for Claude.ai project instructions

## Cowork-Specific Instructions

Skills for the Cowork platform (https://cowork.com) follow similar conventions to Claude Code, but have unique considerations:

1. They use a `skills-rules.json` file (not YAML frontmatter) for metadata
2. These are installed as standalone `.skill` files via the marketplace
3. They have access to `present_files` for packaging results
4. Check Claude Code's latest docs if targeting this platform, as conventions may change
