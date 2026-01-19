---
description: File unfiled tasks from inbox to project notes
allowed-tools: Read, Edit, Glob, Grep, Bash(git:*)
---

# File Inbox Workflow

Process unfiled tasks from the weekly note inbox and daily notes, filing them to appropriate project notes.

## Step 1: Get Active Projects

Read the Active Projects section from `Notes/00 - Projects/TBL.md` to understand what projects are available for filing.

## Step 2: Find Current Week

Determine the current ISO week number and find the weekly note at `Calendar/YYYY-Wnn.md`.

## Step 3: Scan for Unfiled Tasks

Scan these locations for tasks that are not linked to any project:

1. **Current weekly note** - Look for `## Inbox` section, extract tasks without `[[project]]` links
2. **Recent daily notes** - Check `Calendar/YYYYMMDD.md` files from the last 7 days

An unfiled task is:
- A checkbox item `[ ]` or `* ` task
- Does NOT contain a `[[Project Name]]` link
- Is NOT already tagged with `@archived`

## Step 4: Match and Propose Filing

For each unfiled task:
1. Analyze task content for keywords matching active projects
2. Determine confidence level (high/medium/low)
3. If no clear match, mark as "needs manual filing"

## Step 5: Present Filing Plan

Show the Human Partner a summary in this format:

```
## Inbox Filing Proposal

Found N unfiled tasks:

**High confidence:**
1. "Task description" → [[Project Name]]
2. "Task description" → [[Project Name]]

**Needs confirmation:**
3. "Task description" → [[Suggested Project]]? (reason for uncertainty)

**No clear match:**
4. "Task description" → ? (suggest creating project or manual filing)

Proceed with filing? Specify any changes needed.
```

## Step 6: Apply Changes

After Human Partner approval:
1. For each task being filed:
   - Add `[[Project Name]]` link to the task
   - Optionally move task to the project note if requested
2. Remove filed tasks from inbox section
3. Commit changes: `git add -A && git commit -m "file-inbox: filed N tasks to M projects"`

## Notes

- Never delete tasks without explicit permission
- Preserve task formatting (tags, dates, importance markers)
- If uncertain about a match, ask rather than guess
- Update the Inbox section to reflect filed items
