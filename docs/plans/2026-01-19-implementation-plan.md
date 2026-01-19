# NotePlan Plugin Implementation Plan

> **For Claude:** Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a Claude Code plugin that provides productivity workflows for NotePlan.

**Architecture:** Hybrid approach - core workflow logic in plugin, references NotePlan dir for project-specific data.

**Tech Stack:** Python 3, pytest, uv for package management

---

## CRITICAL: Python Environment Requirements

**ALL Python commands MUST use the virtual environment. NO EXCEPTIONS.**

```bash
source .venv/bin/activate && pytest tests/ -v
source .venv/bin/activate && python scripts/extract_session_data.py
```

---

## Task 1: Initialize Python Environment

**Goal:** Set up uv and virtual environment for Python development.

**Steps:**
1. Create virtual environment with uv
2. Install pytest
3. Verify environment works

**Commands:**
```bash
uv venv
source .venv/bin/activate
uv pip install pytest
pytest --version
```

**Verification:** `pytest --version` outputs version info

**Commit:** `git add .venv .python-version && git commit -m "Setup: initialize Python venv with uv"`

---

## Task 2: Create Plugin Manifest

**Goal:** Create the plugin.json manifest.

**File:** `.claude-plugin/plugin.json`

**Content:**
```json
{
  "name": "noteplan",
  "version": "0.1.0",
  "description": "NotePlan productivity workflows for Claude Code",
  "author": {
    "name": "CL"
  }
}
```

**Commit:** `git add .claude-plugin/ && git commit -m "Setup: create plugin manifest"`

---

## Task 3: Copy and Adapt Session Analyzer

**Goal:** Copy extract_session_data.py and tests from noteplan repo.

**Source files:**
- `~/git/noteplan/scripts/extract_session_data.py`
- `~/git/noteplan/tests/test_extract_session_data.py`

**Steps:**
1. Copy script to `scripts/extract_session_data.py`
2. Copy tests to `tests/test_extract_session_data.py`
3. Create `tests/__init__.py`
4. Run tests to verify they pass

**Verification:**
```bash
source .venv/bin/activate && pytest tests/ -v
```

**Commit:** `git add scripts/ tests/ && git commit -m "feat: add session analyzer from noteplan"`

---

## Task 4: Create NotePlan Productivity Skill

**Goal:** Create skill with NotePlan system knowledge.

**File:** `skills/noteplan-productivity/SKILL.md`

**Content should include:**
- Tag scheme: @waiting, @artifact, @chore, @archived
- File naming: YYYYMMDD.md (daily), YYYY-Wnn.md (weekly), YYYY-Qn.md (quarterly)
- Directory structure: Notes/, Calendar/, TBL.md active projects
- Workflow triggers and purposes

**Commit:** `git add skills/ && git commit -m "feat: add noteplan-productivity skill"`

---

## Task 5: Create Commands

**Goal:** Create the 5 workflow commands.

### 5a: file-inbox command
**File:** `commands/file-inbox.md`
**Purpose:** File unfiled tasks from daily/weekly notes to projects
**References:** TBL.md active projects, daily/weekly notes

### 5b: weekly-plan command
**File:** `commands/weekly-plan.md`
**Purpose:** Monday planning workflow
**Includes:** Calendar review, @waiting items, carried over tasks

### 5c: weekly-review command
**File:** `commands/weekly-review.md`
**Purpose:** Friday review workflow
**Includes:** Completed tasks, open tasks, Q1 goal check

### 5d: scan-past-due command
**File:** `commands/scan-past-due.md`
**Purpose:** Find and handle overdue tasks
**Output:** List with options: reschedule, file, mark @waiting, delete

### 5e: analyze-sessions command
**File:** `commands/analyze-sessions.md`
**Purpose:** Run session analyzer and categorize usage
**Uses:** scripts/extract_session_data.py

**Commit after each:** `git add commands/<name>.md && git commit -m "feat: add <name> command"`

---

## Task 6: Create Productivity Assistant Agent

**Goal:** Create agent that proactively suggests workflows.

**File:** `agents/productivity-assistant.md`

**Triggering:** Always when session starts in NotePlan directory

**Behavior:**
- Check current day (Monday → suggest weekly-plan, Friday → suggest weekly-review)
- Mention available workflows
- Check for obvious issues (overdue tasks, unfiled inbox)

**Commit:** `git add agents/ && git commit -m "feat: add productivity-assistant agent"`

---

## Task 7: Create SessionStart Hook

**Goal:** Create hook that activates when session starts in NotePlan dir.

**File:** `hooks/hooks.json`

**Hook type:** Prompt-based (checks context, outputs suggestions)

**Behavior:**
- Detect if in NotePlan directory
- Check for pending reviews or overdue tasks
- Provide brief status and suggestions

**Commit:** `git add hooks/ && git commit -m "feat: add SessionStart hook"`

---

## Task 8: Create .gitignore

**Goal:** Ignore appropriate files.

**File:** `.gitignore`

**Content:**
```
.venv/
__pycache__/
*.pyc
.DS_Store
.claude/*.local.md
*.egg-info/
dist/
build/
```

**Commit:** `git add .gitignore && git commit -m "Setup: add .gitignore"`

---

## Task 9: Create README

**Goal:** Document the plugin for users.

**File:** `README.md`

**Sections:**
- Overview
- Features (commands, skills, agents, hooks)
- Installation
- Usage examples
- Requirements (NotePlan data directory)

**Commit:** `git add README.md && git commit -m "docs: add README"`

---

## Task 10: Validation and Testing

**Goal:** Validate plugin structure and test all components.

**Steps:**
1. Run plugin-validator agent
2. Test each command manually
3. Verify agent triggering
4. Test hook activation
5. Run full test suite

**Verification:**
```bash
source .venv/bin/activate && pytest tests/ -v
```

---

## Summary

10 tasks total:
- Task 1: Python environment setup
- Task 2: Plugin manifest
- Task 3: Session analyzer (copy from noteplan)
- Task 4: NotePlan productivity skill
- Tasks 5a-5e: 5 workflow commands
- Task 6: Productivity assistant agent
- Task 7: SessionStart hook
- Task 8: .gitignore
- Task 9: README
- Task 10: Validation and testing
