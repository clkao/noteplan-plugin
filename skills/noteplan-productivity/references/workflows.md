# NotePlan Workflow Details

## File Inbox Detailed Process

### Step 1: Read Active Projects

Read `Notes/00 - Projects/TBL.md` and extract the Active Projects section:

```markdown
# Active Projects

- [[Project Name 1]] - description
- [[Project Name 2]] - description
```

Parse each line to get project names and descriptions for matching.

### Step 2: Scan Inbox Locations

Check these locations for unfiled tasks:

1. **Current weekly note** (`Calendar/YYYY-Wnn.md`):
   - Look for `## Inbox` section
   - Extract tasks that aren't linked to projects

2. **Recent daily notes** (`Calendar/YYYYMMDD.md`):
   - Check last 7 days
   - Find tasks without `[[project]]` links

### Step 3: Match Tasks to Projects

For each unfiled task:
1. Analyze task content for keywords
2. Match against active project names and descriptions
3. If no clear match, flag for manual filing
4. Suggest most likely project based on context

### Step 4: Present Filing Plan

Show Human Partner a summary:
```
Found 5 unfiled tasks:

1. "Call vendor about contract" → [[Vendor Management]] (high confidence)
2. "Review Q1 metrics" → [[Analytics]] (medium confidence)
3. "Random thought about redesign" → ? (no clear match)

Proceed with filing? [y/n]
```

### Step 5: Apply and Commit

After approval:
1. Move tasks to appropriate project notes
2. Add `[[Project Name]]` links where moved
3. Remove from inbox location
4. Git commit with message: "file-inbox: filed N tasks to M projects"

## Weekly Plan Detailed Process

### Pre-Planning Checklist

Before planning:
- [ ] Review calendar for the week (meetings, deadlines)
- [ ] Check @waiting items - any responses received?
- [ ] Note any blocked tasks that can be unblocked

### Planning Steps

1. **Carried Over Tasks**
   - Read previous week's note
   - Find open tasks (unchecked `[ ]`)
   - Present for carry-over decision

2. **Scheduled This Week**
   - Scan project notes for `>YYYY-Wnn` where nn = current week
   - Scan for `>YYYY-MM-DD` in this week's date range

3. **Past Due Items**
   - Run scan-past-due logic
   - Present items needing reschedule

4. **Inbox Processing**
   - Run file-inbox logic
   - Clear inbox before planning

5. **Priority Setting**
   - Human Partner picks top 3-5 priorities
   - Mark with `!!` or `!!!` for importance

6. **Weekly Note Update**
   - Create or update `Calendar/YYYY-Wnn.md`
   - Add priorities and scheduled tasks

## Weekly Review Detailed Process

### Review Steps

1. **Completed Tasks**
   - Find all `[x]` tasks completed this week
   - Summarize by project
   - Calculate completion rate

2. **Open Tasks**
   - Find unchecked `[ ]` tasks from this week
   - For each: carry over, reschedule, or drop?
   - Dropping = mark `[-]` cancelled

3. **@waiting Review**
   - List all current @waiting items
   - Any updates? Any follow-up needed?
   - Remove @waiting from resolved items

4. **Quarterly Goal Check**
   - Read `Calendar/YYYY-Qn.md`
   - Compare progress against goals
   - Flag any goals at risk

5. **Apply Changes**
   - Update task statuses
   - Add `@archived` to completed items if keeping context
   - Git commit with weekly summary

### Weekly Summary Format

```markdown
## Week N Review

**Completed:** X tasks across Y projects
**Carried over:** Z tasks
**Goals:** On track / At risk

Notable completions:
- [x] Major task 1
- [x] Major task 2

Carried to next week:
- [ ] Task 1 (reason)
- [ ] Task 2 (reason)
```

## Scan Past Due Detailed Process

### Scanning Logic

Search all notes for:

```
# Pattern 1: Scheduled before current week
>YYYY-MM-DD where date < today
>YYYY-Wnn where week < current week

# Pattern 2: Orphan tasks
[ ] Task without [[project]] link and no >date
```

### Action Options

For each past-due item:

| Option | Action |
|--------|--------|
| Reschedule | Add new `>date`, remove old |
| File | Move to project note |
| @waiting | Add tag, note who blocking |
| Delete | Remove task entirely |

### Batch Processing

Present items in batches of 5-10 for easier processing:
```
Past due items (batch 1 of 3):

1. [ ] Task from 2 weeks ago >2026-01-05
   Options: [r]eschedule, [f]ile, [w]aiting, [d]elete

2. [ ] Orphan task (no date, no project)
   Options: [r]eschedule, [f]ile, [w]aiting, [d]elete
```
