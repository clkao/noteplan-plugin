# NotePlan Companion Plugin

A Claude Code plugin that provides productivity workflows for NotePlan.

## Overview

This plugin wraps CL's NotePlan productivity system, providing:
- Slash commands for workflows (file-inbox, weekly-plan, weekly-review, scan-past-due, analyze-sessions)
- Skills for NotePlan system knowledge (tag scheme, file naming, structure)
- Proactive productivity assistant agent
- Session analyzer for Claude Code usage tracking

## Plugin Architecture

**Hybrid approach:** Core workflow logic lives in the plugin, but commands reference the NotePlan data directory for project-specific details (TBL.md active projects, templates, calendar files).

**NotePlan directory:** `~/git/noteplan` (symlink to NotePlan data)

## Python Environment

**CRITICAL: ALL Python commands MUST use the virtual environment.**

```bash
# Setup (one time)
uv venv
source .venv/bin/activate
uv pip install pytest

# Running Python
source .venv/bin/activate && pytest tests/ -v
source .venv/bin/activate && python scripts/extract_session_data.py --week W03
```

**Package management uses uv:**
```bash
uv pip install <package>
```

**NEVER run Python without activating venv first.**

## Development Rules

### Test Driven Development

For EVERY feature or bugfix:
1. Write a failing test that validates desired functionality
2. Run test to confirm it fails
3. Write ONLY enough code to make test pass
4. Run test to confirm success
5. Refactor if needed while keeping tests green

### Code Style

- Match surrounding code style
- ABOUTME comments at top of every file (2 lines, each starting with "ABOUTME:")
- No temporal comments ("new", "improved", "refactored")
- Names describe what code does, not implementation details

### Git

- Commit frequently throughout development
- Never skip pre-commit hooks
- Use `git status` before `git add -A`

## Components

### Commands (5)
- `file-inbox` - File unfiled tasks from daily/weekly notes to projects
- `weekly-plan` - Monday planning workflow
- `weekly-review` - Friday review workflow
- `scan-past-due` - Find and handle overdue tasks
- `analyze-sessions` - Claude Code usage analysis

### Skills (1)
- `noteplan-productivity` - Tag scheme, file naming, directory structure, workflows

### Agents (1)
- `productivity-assistant` - Proactively suggests workflows when in NotePlan dir

### Hooks (1)
- `SessionStart` - Check for overdue tasks or pending reviews

### Scripts (1)
- `extract_session_data.py` - Python session analyzer with tests

## Testing

```bash
# Run all tests
source .venv/bin/activate && pytest tests/ -v

# Run specific test
source .venv/bin/activate && pytest tests/test_extract_session_data.py -v
```

## Directory Structure

```
noteplan-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/                 # Slash commands
├── agents/                   # Subagent definitions
├── skills/
│   └── noteplan-productivity/
│       └── SKILL.md
├── hooks/
│   └── hooks.json
├── scripts/
│   └── extract_session_data.py
├── tests/
│   └── test_extract_session_data.py
└── docs/
    └── plans/
