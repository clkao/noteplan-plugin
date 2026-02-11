---
description: Weekly review workflow to close out the week
allowed-tools: Read, Edit, Glob, Grep, Bash(git:*)
---

# Weekly Review Workflow

End-of-week reflection and cleanup. Best run on Friday.

## Step 1: Gather Context

Determine current ISO week and read:

- **This week's note**: `Calendar/YYYY-Wnn.md`
- **Daily notes from this week**: `Calendar/YYYYMMDD.md`
- **Quarterly goals**: `Calendar/YYYY-Q1.md`

Also grep for `@done(YYYY-MM-DD` with dates in this week to find all completed tasks across all notes.

## Step 2: Summarize Completed Tasks

Find all completed tasks `[x]` from this week across all notes.

Present summary:
```
## Completed This Week

**By Project:**
- [[Project A]]: 5 tasks completed
  - [x] Task 1
  - [x] Task 2
- [[Project B]]: 3 tasks completed
  ...

**Total:** N tasks completed across M projects

Celebrate wins!
```

## Step 3: Review Open Tasks

Find all unchecked tasks `[ ]` scheduled for this week across project notes and the weekly note. Group by project and present in batches of 5-10:

```
## Open Tasks (Batch 1 of N — [[Project A]])

1. [ ] Task description
   → Carry to next week / Reschedule to date / Drop / Mark @waiting

2. [ ] Task description
   → Carry to next week / Reschedule to date / Drop / Mark @waiting

Running tally: X carried, Y rescheduled, Z dropped
```

Get decisions on each batch before proceeding to the next. After all batches, show final tally.

## Step 4: Review @waiting Items

Find all tasks tagged `@waiting`:

```
## Waiting Items

These are blocked on others:

1. [ ] Task @waiting (waiting on: person/thing)
   - Still waiting? Remove @waiting? Follow up needed?

2. [ ] Task @waiting
   - Any update?
```

## Step 5: Clean Up Daily Notes

For each daily note from this week, check for leftover tasks:

**Synced lines** (tasks with `^blockid`):
- These already exist in the source project note
- Remove them from the daily note - they're duplicates

**Standalone tasks** (no `^blockid`):
- File to appropriate project note with scheduling (e.g., `>YYYY-W(nn+1)`)
- Ask Human Partner where they belong if unclear

## Step 6: Find and Move Straggler Tasks

Grep for `>YYYY-Wnn` (this week) across ALL notes to find unmoved tasks:

- Reschedule open tasks to next week (`>YYYY-W(nn+1)`)
- **Weekly note chores**: Move unmoved chores to next week's weekly note (NOT to project notes)

## Step 7: Quarterly Goal Check

Read `Calendar/YYYY-Q1.md` (or current quarter). Check progress:

```
## Q1 Goal Check

**Goals:**
- [ ] Goal 1: [On track / Behind / Blocked]
- [ ] Goal 2: [On track / Behind / Blocked]

What would move the needle next week?
Any adjustments needed?
```

## Step 8: Goal Tracking and Reflection

Read the quarterly goals from `Calendar/YYYY-Qn.md`. For each goal that has measurable targets, ask the Human Partner for this week's data. Derive the prompts from whatever goals are currently set — do not hardcode specific metrics.

Then prompt for reflections:

```
- Great: What went well this week?
- Tricky: What was hard or frustrating?
- Change: What would you do differently?
```

Include this data in the quarterly review entry and in the weekly summary (Step 10).

## Step 9: Update Next Week's Note

If next week's note exists, update it with:

- **Synced tasks** (with `^blockid`): Can add to weekly note WITH the identifier - they will sync
  - KEEP the `>YYYY-Wnn` scheduling in the project file - don't remove it
- **Scheduled-only tasks** (no `^blockid`): Do NOT duplicate - they're already in project notes
  - Carryover is documented in review notes instead

## Step 10: Generate Weekly Summary

Add to this week's note. Include goal-tracking data from Step 8:

```markdown
## W(nn) Review Notes (YYYY-MM-DD)

**Goal tracking:** (metrics from Step 8, matching quarterly goal targets)

**Wins:** accomplishment1, accomplishment2, accomplishment3

**Tricky:** challenge1, challenge2

**Carried to W(nn+1):** task1, task2, task3
```

## Step 11: Commit

```bash
git add -A && git commit -m "weekly-review: W(nn) - X completed, Y carried"
```

## Notes

- This workflow is typically run on Friday
- Focus on reflection and closure, not planning
- Celebrate completions - acknowledge progress made
- If Claude Code session analysis is desired, suggest running `/noteplan:analyze-sessions`
- Goal tracking metrics are prompted in Step 8 based on quarterly goals
