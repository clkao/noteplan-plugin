---
description: File unfiled tasks from inbox to project notes
allowed-tools: Read, Edit, Glob, Grep, Bash(git:*)
---

# File Inbox Workflow

Scan inbox for unfiled tasks and propose where to file them.

## Step 1: Get Active Projects

Read the Active Projects section from `Notes/00 - Projects/TBL.md` to understand what projects are available for filing.

## Step 2: Find Current Week

Determine the current ISO week number and find the weekly note at `Calendar/YYYY-Wnn.md`.

## Step 3: Scan for Unfiled Tasks

Scan these locations **in order of priority**:

1. **Weekly notes (main focus)** - Current and recent week's notes get messy
   - Look for tasks NOT linked to a project or scheduled
   - Items without NotePlan sync IDs (`^xxxxx`) are often unfiled

2. **TBL.md (below Active Projects section)** - Often has accumulated unfiled tasks and duplicates
   - Check for items that should be in project notes

3. **Daily notes** - SKIP unless explicitly asked
   - Daily note tasks are already scheduled to that day
   - Only scan `## Inbox` section if it exists

An unfiled task is:
- A checkbox item `[ ]` or `* ` task
- Does NOT contain a `[[Project Name]]` link
- Does NOT have a sync ID (`^xxxxx`) linking it elsewhere
- Is NOT already tagged with `@archived`

## Step 4: Categorize and Match Tasks

For each unfiled task, categorize by type:

| Category | Typical Destination |
|----------|---------------------|
| Work tasks | Appropriate work project based on keywords |
| Random ideas, side projects | `Notes/Ideas.md` |
| Personal errands | Weekly note `## Chores` section |
| Personal/family tasks | Personal project notes |
| Recurring daily tasks | Leave in weekly note (e.g., "schedule comm") |

Determine confidence level (high/medium/low) for each match.

## Step 5: Present Filing Plan

Show the Human Partner a summary grouped by destination:

```
## Inbox Filing Proposal

Found N unfiled tasks:

→ [[Project A]]:
- task description
- another task

→ [[Project B]]:
- task description

→ [[Ideas]]:
- random thought
- side project idea

→ Weekly Chores:
- personal errand

→ Unclear (need input):
- ambiguous task

Proceed with filing? Specify any changes needed.
```

## Step 6: Apply Changes

After Human Partner approval, for each task being filed:

1. **Move the task to the destination project note**
   - Add to appropriate section in the project file
   - Include scheduling: `>YYYY-Wnn` for the current or next week
   - **IMPORTANT: Preserve all sub-items and notes** - don't lose context

2. **Remove the task from its source location**
   - Delete from inbox/weekly note/TBL.md after moving

3. **For Ideas.md**: Just add to appropriate section, no scheduling needed

4. **Commit changes**: `git add -A && git commit -m "file-inbox: filed N tasks to M projects"`

## Notes

- Never delete tasks without explicit permission
- Preserve task formatting (tags, dates, importance markers, sub-items)
- If uncertain about a match, ask rather than guess
- Watch for tasks with detailed sub-notes (like fee requirements) - preserve them!
- If many tasks cluster around a theme, suggest creating a new project
- Tasks with sync IDs (`^xxxxx`) may already be synced elsewhere - check before moving
