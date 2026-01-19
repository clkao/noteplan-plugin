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

Find unchecked tasks `[ ]` from this week's note. For each, ask:

```
## Open Tasks

These tasks are still open from this week:

1. [ ] Task description (from [[Project]])
   → Carry to next week / Reschedule to date / Drop / Mark @waiting

2. [ ] Task description (orphan)
   → Carry to next week / File to project / Drop
```

Process Human Partner's decisions for each task.

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

## Step 8: Update Next Week's Note

If next week's note exists, update it with:

- **Synced tasks** (with `^blockid`): Can add to weekly note WITH the identifier - they will sync
  - KEEP the `>YYYY-Wnn` scheduling in the project file - don't remove it
- **Scheduled-only tasks** (no `^blockid`): Do NOT duplicate - they're already in project notes
  - Carryover is documented in review notes instead

## Step 9: Generate Weekly Summary

Add to this week's note:

```markdown
## W(nn) Review Notes (YYYY-MM-DD)

**Wins:** accomplishment1, accomplishment2, accomplishment3

**Carried to W(nn+1):** task1, task2, task3
```

## Step 10: Commit

```bash
git add -A && git commit -m "weekly-review: W(nn) - X completed, Y carried"
```

## Notes

- This workflow is typically run on Friday
- Focus on reflection and closure, not planning
- Celebrate completions - acknowledge progress made
- If Claude Code session analysis is desired, suggest running `/noteplan:analyze-sessions`
- Health metrics (exercise, meditation, weight) can be logged in `## Health` section if Human Partner tracks them
