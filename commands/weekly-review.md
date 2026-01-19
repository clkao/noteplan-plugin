---
description: Weekly review workflow to close out the week
allowed-tools: Read, Edit, Glob, Grep, Bash(git:*)
---

# Weekly Review Workflow

Review the week's progress, close out completed work, and prepare for next week.

## Step 1: Find This Week's Note

Determine current ISO week. Read `Calendar/YYYY-Wnn.md`.

## Step 2: Summarize Completed Tasks

Find all completed tasks `[x]` from this week across:
- Weekly note
- Daily notes from this week
- Project notes (tasks completed this week)

Present summary:

```
## Completed This Week

**By Project:**
- [[Project A]]: 5 tasks completed
  - [x] Task 1
  - [x] Task 2
  ...
- [[Project B]]: 3 tasks completed
  ...

**Total:** N tasks completed across M projects
```

## Step 3: Review Open Tasks

Find unchecked tasks `[ ]` from this week. For each, ask:

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

## Step 5: Quarterly Goal Check

Read `Calendar/YYYY-Q1.md` (or current quarter). Check progress against goals:

```
## Q1 Goal Check

**Goals from Q1:**
- [ ] Goal 1: [status - on track / at risk / blocked]
- [ ] Goal 2: [status]

Any adjustments needed?
```

## Step 6: Generate Weekly Summary

Create a summary to add to the weekly note:

```markdown
## Week NN Review

**Completed:** X tasks across Y projects
**Carried over:** Z tasks to next week
**Blocked:** N items @waiting

### Highlights
- Major accomplishment 1
- Major accomplishment 2

### Carried to Next Week
- [ ] Task 1
- [ ] Task 2
```

## Step 7: Apply Changes

1. Update task statuses in weekly and project notes
2. Add `@archived` tag to completed tasks if Human Partner wants to preserve context
3. Carry tasks to next week's note if it exists
4. Update weekly note with review summary

## Step 8: Commit

```bash
git add -A && git commit -m "weekly-review: completed X tasks, carried Y to next week"
```

## Notes

- This workflow is typically run on Friday
- Focus on reflection and closure, not planning
- Celebrate completions - acknowledge progress made
- If Claude Code session analysis is desired, suggest running `/noteplan:analyze-sessions`
