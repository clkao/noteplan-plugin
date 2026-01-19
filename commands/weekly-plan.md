---
description: Weekly planning workflow for the upcoming week
allowed-tools: Read, Edit, Glob, Grep, Bash(git:*)
---

# Weekly Plan Workflow

Plan the upcoming week by reviewing carried-over tasks, scheduled items, and setting priorities.

## Pre-Planning Checklist

Before planning, help the Human Partner review:

1. **Calendar for the week** - Any meetings, deadlines, or commitments?
2. **@waiting items** - Any responses received that unblock work?
3. **Blocked tasks** - Anything that can now proceed?

Ask about these briefly before proceeding.

## Step 1: Find Previous Week

Determine current ISO week. Read the previous week's note `Calendar/YYYY-W(nn-1).md`.

## Step 2: Show Carried Over Tasks

Find unchecked tasks `[ ]` from previous week's note. Present as:

```
## Carried Over from Last Week

[ ] Task 1 (from [[Project A]])
[ ] Task 2 (from [[Project B]])
[ ] Task 3 (orphan - no project)

Which of these should carry forward to this week?
```

## Step 3: Show Scheduled This Week

Search project notes and calendar for tasks scheduled this week:
- Tasks with `>YYYY-Wnn` where nn = current week
- Tasks with `>YYYY-MM-DD` in this week's date range

Present these as scheduled work for the week.

## Step 4: Surface Past Due Items

Scan for tasks scheduled before current week that are still open:
- `>YYYY-MM-DD` where date < today
- `>YYYY-Wnn` where week < current week

Present with options: reschedule, drop, or mark @waiting.

## Step 5: Process Inbox

Check for unfiled tasks in:
- Current weekly note's Inbox section
- Recent daily notes

Suggest filing or ask if Human Partner wants to run `/noteplan:file-inbox`.

## Step 6: Set Priorities

Ask the Human Partner to pick top 3-5 priorities for the week:

```
## This Week's Priorities

Based on carried over tasks, scheduled work, and past due items:

What are your top priorities for this week?
(I'll mark these with !! for importance)
```

## Step 7: Create/Update Weekly Note

Create or update `Calendar/YYYY-Wnn.md` with:

```markdown
# Week NN - YYYY

## Priorities
- [ ] Priority 1 !!
- [ ] Priority 2 !!
- [ ] Priority 3

## Scheduled
- [ ] Scheduled task 1
- [ ] Scheduled task 2

## Inbox
(empty after filing)

## Notes
```

## Step 8: Commit

After changes are complete:
```bash
git add -A && git commit -m "weekly-plan: set up W(nn) with N priorities"
```

## Notes

- This workflow is typically run on Monday
- Focus on helping Human Partner make decisions, not making them for them
- Keep the planning session focused - avoid going deep into individual tasks
- Reference Q1 goals from `Calendar/YYYY-Q1.md` if relevant
