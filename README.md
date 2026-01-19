# NotePlan Companion Plugin

A Claude Code plugin that provides productivity workflows for NotePlan.

## Features

### Commands

| Command | Description |
|---------|-------------|
| `/noteplan:file-inbox` | File unfiled tasks from inbox to project notes |
| `/noteplan:weekly-plan` | Plan the upcoming week (best on Monday) |
| `/noteplan:weekly-review` | Review and close out the week (best on Friday) |
| `/noteplan:scan-past-due` | Find and handle overdue tasks |
| `/noteplan:analyze-sessions` | Analyze Claude Code usage for weekly review |

### Skills

- **noteplan-productivity** - Knowledge of the NotePlan productivity system including tag scheme, file naming conventions, and workflows

### Agents

- **productivity-assistant** - Proactively suggests workflows when in NotePlan directory based on day of week and context

### Hooks

- **SessionStart** - Detects NotePlan directory and reminds about available workflows

## Installation

### Option 1: Local Plugin Directory

```bash
# From Claude Code
cc --plugin-dir /path/to/noteplan-plugin
```

### Option 2: Copy to Project

```bash
cp -r noteplan-plugin /your/noteplan/dir/.claude-plugin
```

## Requirements

- Must be run from within the NotePlan data directory (or a symlink to it)
- NotePlan data directory should have:
  - `Notes/00 - Projects/TBL.md` with Active Projects section
  - `Calendar/` directory with daily/weekly notes
  - `CLAUDE.md` for context

## Tag Scheme

| Tag | Meaning |
|-----|---------|
| `@waiting` | Blocked, ball in someone else's court |
| `@artifact` | Deep work, produces deliverable |
| `@chore` | Maintenance, recurring |
| `@archived` | Completed, kept for context |

## File Naming

| Type | Format | Example |
|------|--------|---------|
| Daily | `YYYYMMDD.md` | `20260119.md` |
| Weekly | `YYYY-Wnn.md` | `2026-W03.md` |
| Quarterly | `YYYY-Qn.md` | `2026-Q1.md` |

## Session Analyzer

The plugin includes a Python script for analyzing Claude Code session data. It uses only Python stdlib, so no installation is needed:

```bash
# Run analysis (no setup required - uses Python stdlib only)
python3 scripts/extract_session_data.py --week W03
```

### Development Setup

For running tests during development:

```bash
uv venv
source .venv/bin/activate
uv pip install pytest
pytest tests/ -v
```

### Session Categories

| Category | Keywords |
|----------|----------|
| `review` | weekly review, scan past due |
| `planning` | weekly plan, priorities |
| `skill-dev` | skill, command, script |
| `organization` | file inbox, filing |
| `content` | write, notes, documentation |
| `coding` | code, fix, bug, test |
| `exploration` | what, how, find |

## Development

### Running Tests

```bash
source .venv/bin/activate && pytest tests/ -v
```

### Project Structure

```
noteplan-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/                 # Slash commands
│   ├── file-inbox.md
│   ├── weekly-plan.md
│   ├── weekly-review.md
│   ├── scan-past-due.md
│   └── analyze-sessions.md
├── agents/
│   └── productivity-assistant.md
├── skills/
│   └── noteplan-productivity/
│       ├── SKILL.md
│       └── references/
├── hooks/
│   └── hooks.json
├── scripts/
│   └── extract_session_data.py
├── tests/
│   └── test_extract_session_data.py
├── CLAUDE.md
└── README.md
```

## License

MIT
