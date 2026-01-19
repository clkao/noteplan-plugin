---
name: NotePlan Productivity
description: This skill should be used when the user asks about "NotePlan", "weekly review", "weekly plan", "file inbox", "scan past due", "@waiting tasks", "@artifact tasks", "TBL", "active projects", or mentions NotePlan tags (@waiting, @artifact, @chore, @archived). Provides knowledge of CL's NotePlan productivity system including tag scheme, file naming, directory structure, and workflows.
version: 0.1.0
---

# NotePlan Productivity System

## Overview

The Human Partner's NotePlan productivity system organizes tasks and notes with Git version control and Claude Code integration. The system uses a tag scheme for task categorization, standardized file naming, and defined workflows for planning and review.

**Announce at start:** "I'm using the NotePlan productivity skill to help with your productivity workflows."

## Core Concepts

### Tag Scheme

| Tag | Meaning | Use Case |
|-----|---------|----------|
| `@waiting` | Blocked, ball in someone else's court | Follow-ups, pending responses |
| `@artifact` | Deep work, produces deliverable | OSR items, concentration work |
| `@chore` | Maintenance, recurring | Admin, cleanup, no end state |
| `@archived` | Completed, kept for context | Preserves hierarchy in notes |

**Existing NotePlan features (unchanged):**
- `!`, `!!`, `!!!` for importance
- `>YYYY-MM-DD` or `>YYYY-Wnn` for scheduling
- `[x]` completed, `[-]` cancelled
- `[[Note Name]]` for linking

### File Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Daily | `YYYYMMDD.md` | `20260119.md` |
| Weekly | `YYYY-Wnn.md` | `2026-W03.md` |
| Quarterly | `YYYY-Qn.md` | `2026-Q1.md` |

### Directory Structure

```
NotePlan/
├── Calendar/           # Daily, weekly, quarterly notes
├── Notes/
│   ├── 00 - Projects/  # Project notes
│   │   └── TBL.md      # Big List with Active Projects
│   └── 📋 Templates/   # Note templates
├── commands/           # Claude workflow commands
└── Filters/            # Saved views
```

### Active Projects (TBL.md)

The Big List (`Notes/00 - Projects/TBL.md`) contains the **Active Projects** section at the top. Read this list to determine where to file tasks.

Format:
```markdown
# Active Projects

- [[Project Name 1]] - brief description
- [[Project Name 2]] - brief description
```

Projects not on this list are considered inactive/archived.

## Workflows

### File Inbox

**Purpose:** File unfiled tasks from daily/weekly notes to appropriate project notes.

**Process:**
1. Read TBL.md to get active projects list
2. Scan current weekly note's Inbox section
3. Scan recent daily notes for unlinked tasks
4. Match each task to an active project based on content
5. Present proposed filing to user for approval
6. Apply changes and commit to git

**Triggers:** "file inbox", "file my inbox", "process inbox"

### Weekly Plan (Monday)

**Purpose:** Plan the upcoming week by reviewing carried-over tasks and setting priorities.

**Process:**
1. Show tasks carried over from previous week
2. Show tasks scheduled for this week from project notes
3. Surface past-due items needing reschedule
4. Check for orphan tasks in inbox
5. Review @waiting items for follow-up
6. User picks priorities
7. File inbox items, update project notes
8. Git commit

**Pre-planning prompts:**
- Review calendar for the week
- Check @waiting items for follow-up
- Consider any blocked tasks

**Triggers:** "weekly plan", "plan the week", "Monday planning"

### Weekly Review (Friday)

**Purpose:** Review the week's progress and prepare for next week.

**Process:**
1. Show completed tasks this week
2. Show open tasks - carry over, reschedule, or drop?
3. Review @waiting items - any updates?
4. Q1 goal check: "On track?"
5. User marks @archived, reschedules, or flags
6. Apply changes and commit with summary

**Triggers:** "weekly review", "review the week", "Friday review"

### Scan Past Due

**Purpose:** Find and handle tasks scheduled before current week.

**Process:**
1. Scan all notes for:
   - Open tasks scheduled before current week
   - Tasks with no project link and no schedule
2. Present list with options per item:
   - Reschedule to specific date/week
   - File to a project
   - Mark @waiting
   - Delete
3. User decides per item
4. Apply changes and commit

**Triggers:** "scan past due", "find overdue", "scan overdue"

### Analyze Sessions

**Purpose:** Analyze Claude Code session data for weekly review.

**Process:**
1. Run session extraction script for specified period
2. Classify sessions by category (review, planning, skill-dev, organization, content, coding, exploration)
3. Detect phases within sessions based on message transitions
4. Aggregate metrics by category
5. Output markdown summary for weekly note

**Categories:**

| Category | Keywords |
|----------|----------|
| `review` | weekly review, scan past due, checking progress |
| `planning` | weekly plan, priorities, scheduling |
| `skill-dev` | skill, command, template, script, hook |
| `organization` | file inbox, filing, moving tasks, cleanup |
| `content` | write, writing, notes, documentation |
| `coding` | implement, code, fix, bug, test, debug |
| `exploration` | what, how, where, find, search, understand |

**Triggers:** "analyze sessions", "session analysis", "Claude usage"

## Hybrid Architecture

This plugin uses a hybrid approach:
- **Core workflow logic** lives in the plugin commands
- **Project-specific data** is read from the NotePlan directory at runtime:
  - Active projects from TBL.md
  - Templates from Notes/📋 Templates/
  - Current calendar files

**NotePlan directory path:** The plugin expects to be run from within the NotePlan data directory or a symlink to it (e.g., `~/git/noteplan`).

## Git Integration

All changes made by workflows are committed to git:
- Commit after filing/archiving changes
- Descriptive commit messages explaining what changed
- Full history available via `git log` and `git diff`
- Never force push or rewrite history

## Time Horizons

```
Yearly (2026.md) - optional, light reflection
  └── Quarterly (2026-Q1.md) - goals, success criteria, active projects
        └── Weekly (2026-W02.md) - tactical priorities, scheduled tasks
              └── Daily (20260111.md) - execution, inbox capture
```

## Additional Resources

### Reference Files

For detailed information, consult:
- **`references/workflows.md`** - Detailed workflow procedures
- **`references/categories.md`** - Session analysis category definitions

### Scripts

- **`${CLAUDE_PLUGIN_ROOT}/scripts/extract_session_data.py`** - Session data extraction

## Quick Reference

**Common tasks:**

| Task | Action |
|------|--------|
| File a captured task | Match to active project in TBL.md, move to project note |
| Check what's due | Scan Calendar/ for past-due scheduled tasks |
| Find active projects | Read Active Projects section of TBL.md |
| Mark task blocked | Add `@waiting` tag |
| Archive completed | Add `@archived` tag (keeps context) |
| Schedule for later | Add `>YYYY-MM-DD` or `>YYYY-Wnn` |
