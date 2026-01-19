---
description: Find and handle overdue/orphan tasks
allowed-tools: Read, Edit, Glob, Grep, Bash(git:*)
---

# Scan Past Due Workflow

Find tasks that are past their scheduled date or have no project assignment, and help process them.

## Step 1: Determine Current Date Context

Get today's date and current ISO week number for comparison.

## Step 2: Scan for Past Due Tasks

Search all notes for tasks scheduled before today:

**Patterns to find:**
- `[ ]` tasks with `>YYYY-MM-DD` where date < today
- `[ ]` tasks with `>YYYY-Wnn` where week < current week

**Exclude:**
- Completed tasks `[x]`
- Cancelled tasks `[-]`
- Tasks with `@archived` tag

## Step 3: Scan for Orphan Tasks

Find tasks that have no project link, no schedule, and no categorizing tag:

**Criteria:**
- Is a checkbox `[ ]` or task `* `
- Does NOT contain `[[Project Name]]` link
- Does NOT have `>date` or `>week` scheduling
- Does NOT have a categorizing tag (`@waiting`, `@artifact`, `@chore`)
- Is NOT in a project note (under `Notes/00 - Projects/`)

## Step 4: Present Findings

Show results in batches of 5-10 for easier processing:

```
## Past Due Tasks (Batch 1 of N)

**Overdue by date:**
1. [ ] "Task description" - scheduled >2026-01-05 (14 days ago)
   Location: Calendar/20260105.md
   Options: [R]eschedule | [F]ile to project | [W]aiting | [X] done | [D]rop

2. [ ] "Task description" - scheduled >2026-W01 (2 weeks ago)
   Location: Notes/00 - Projects/SomeProject.md
   Options: [R]eschedule | [W]aiting | [X] done | [D]rop

**Orphan tasks (no project, no date, no tag):**
3. [ ] "Task description"
   Location: Calendar/20260110.md
   Options: [R]eschedule | [F]ile to project | [X] done | [D]rop

How would you like to handle each? (e.g., "1R 2W 3F")
```

## Step 5: Process Decisions

For each task based on Human Partner's choice:

**[R]eschedule:**
- Ask for new date or week: "Reschedule to when? (e.g., >2026-01-25 or >2026-W05)"
- Update the task's schedule tag

**[F]ile to project:**
- Show active projects list from TBL.md
- Ask which project
- Add `[[Project Name]]` link to task

**[W]aiting:**
- Add `@waiting` tag
- Ask: "Waiting on whom/what?"
- Add note if provided

**[X] done:**
- Task was actually completed but not checked off
- Mark as `[x]` with `@done(YYYY-MM-DD)` timestamp

**[D]rop:**
- Confirm: "Delete task or mark cancelled [-]?"
- Apply chosen action

## Step 6: Continue or Complete

After processing a batch:
- If more batches remain: "Process next batch? (Y batches remaining)"
- If complete: Summarize changes made

## Step 7: Commit Changes

```bash
git add -A && git commit -m "scan-past-due: processed N tasks (X rescheduled, Y filed, Z dropped)"
```

## Summary Statistics

At the end, show:

```
## Scan Complete

**Processed:** N tasks total
- Rescheduled: X
- Filed to projects: Y
- Marked @waiting: Z
- Marked done: A
- Dropped/cancelled: W

**Still pending:** M tasks (if any skipped)
```

## Notes

- Process in batches to avoid overwhelming Human Partner
- Always confirm before dropping/deleting tasks
- Suggest reasonable reschedule dates based on task content
- If a task keeps getting rescheduled repeatedly, flag it for discussion
