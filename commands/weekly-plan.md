---
description: Weekly planning workflow for the upcoming week
allowed-tools: Read, Edit, Glob, Grep, Bash(git:*)
---

# Weekly Plan Workflow

Start-of-week planning session. Best run on Monday.

## Pre-Planning Prompts

Before planning, remind the Human Partner to:

1. **Check calendar** -2/+4 weeks for upcoming commitments and recent events
2. **Clear physical inbox** - Process any paper items
3. **Clean desktop / downloads folder** - Digital hygiene

Ask briefly about these before proceeding.

## Step 1: Gather Context

Read these files to understand current state:

- **Last week's note**: `Calendar/YYYY-W(nn-1).md`
- **This week's note**: `Calendar/YYYY-Wnn.md` (may not exist yet)
- **Quarterly goals**: `Calendar/YYYY-Q1.md` (or current quarter)
- **Active projects**: `Notes/00 - Projects/TBL.md`

## Step 2: Present Summary

Show the Human Partner a consolidated view:

### Carryover from Last Week

Open tasks from last week's note that weren't completed:
```
[ ] Task description (from last week)
```

### Scheduled for This Week

Tasks from project notes scheduled `>YYYY-Wnn` (this week) or to specific dates this week.

### Past Due

Tasks scheduled before this week that are still open:
```
[ ] Task (was due YYYY-MM-DD)
```

### Inbox Items

Unfiled tasks from daily notes / inbox sections.

### Waiting Items

Open tasks tagged `@waiting` that may need follow-up.

### Q1 Goal Check

Quick status on each quarterly goal:
- Goal 1: On track? / Needs attention?
- Goal 2: On track? / Needs attention?

## Step 3: Help Prioritize

Ask the Human Partner:

```
What are your top 3 priorities this week?
```

Suggest moving past-due items to this week or dropping them.

## Step 4: Update Notes

1. **Create this week's note** if needed (use weekly template if available)
2. **Move carryover tasks** to new week or mark dropped
3. **File inbox items** - run `/noteplan:file-inbox` if needed
4. **Add priorities** to weekly note with `!!` importance markers

Weekly note structure:
```markdown
# Week NN

## Priorities
- [ ] !! Priority 1
- [ ] !! Priority 2
- [ ] Priority 3

## Chores
- [ ] ...

## Inbox
(empty after filing)

## Notes
```

## Step 5: Commit

After changes are complete:
```bash
git add -A && git commit -m "weekly-plan: set up W(nn) with N priorities"
```

## Notes

- This workflow is typically run on Monday
- Focus on helping Human Partner make decisions, not making them for them
- Keep the planning session focused - avoid going deep into individual tasks
- Reference quarterly goals to ensure week aligns with larger objectives
