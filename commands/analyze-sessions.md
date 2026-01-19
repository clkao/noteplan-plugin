---
description: Analyze Claude Code session data for weekly review
argument-hint: [week|date-range]
allowed-tools: Read, Bash(python:*,source:*)
---

# Analyze Sessions Workflow

Analyze Claude Code session data to categorize work and produce a usage summary for weekly review.

## Step 1: Determine Date Range

Parse arguments to determine the analysis period:

- No argument: Current week
- `W03` or `2026-W03`: Specific week
- `2026-01-13 2026-01-19`: Date range

If $ARGUMENTS is provided, use it to set the period.

## Step 2: Run Session Extraction

Execute the session data extraction script:

```bash
source ${CLAUDE_PLUGIN_ROOT}/.venv/bin/activate && python ${CLAUDE_PLUGIN_ROOT}/scripts/extract_session_data.py --week WEEK
```

Or for date range:
```bash
source ${CLAUDE_PLUGIN_ROOT}/.venv/bin/activate && python ${CLAUDE_PLUGIN_ROOT}/scripts/extract_session_data.py --since START --until END
```

Capture the JSON output.

## Step 3: Classify Sessions

For each session in the output, classify based on `firstPrompt` and `userMessages`:

| Category | Keywords |
|----------|----------|
| `review` | weekly review, scan past due, checking progress, review |
| `planning` | weekly plan, plan, priorities, scheduling, reprioritize |
| `skill-dev` | skill, command, template, script, hook, agent, implement |
| `organization` | file inbox, filing, moving tasks, cleanup, organize, carry |
| `content` | write, writing, notes, documentation, draft |
| `coding` | code, fix, bug, test, debug, python, implement |
| `exploration` | what, how, where, find, search, understand, explore |

If ambiguous, default to `exploration`.

## Step 4: Detect Phases (Optional)

For sessions with `messagesWithTimestamps`, detect phase transitions:

**Transition signals:**
- Explicit: "now let's...", "moving on to...", "next:", "ok, let's..."
- Category change based on keywords

**Calculate phase duration:**
- Phase start = first message timestamp
- Phase end = next phase start (or session end for last phase)
- Allocate tokens proportionally by duration

## Step 5: Aggregate Metrics

Sum metrics by category:
- Total duration (minutes)
- Total tokens (input + output + cache_read)
- Phase count
- Activity descriptions

## Step 6: Generate Summary

Output markdown summary:

```markdown
## Claude Code Usage

**Period:** YYYY-Wnn (Mon DD - Mon DD)
**Total time:** Xh Ym | **Tokens:** Nk

| Category     | Time    | Tokens  | Phases | Activities |
|--------------|---------|---------|--------|------------|
| review       | Xh Ym   | Nk      | N      | weekly review, scan overdue |
| skill-dev    | Xh Ym   | Nk      | N      | session analyzer, command work |
| planning     | Xh Ym   | Nk      | N      | weekly plan |
| organization | Xh Ym   | Nk      | N      | file inbox |
| coding       | Xh Ym   | Nk      | N      | bug fixes, scripts |
| exploration  | Xh Ym   | Nk      | N      | codebase exploration |

**Session breakdown:**
- project "first prompt" (Xh Ym): cat1 → cat2 → cat3
- project "first prompt" (Xh Ym): cat1

**Notable sessions:** (top 3 by duration)
- `category` project: "first prompt" - Xh Ym, Nk tokens
```

## Step 7: Present to Human Partner

Show the summary and ask:

```
Would you like me to:
1. Add this summary to this week's note?
2. Show more detail on any category?
3. Compare to previous weeks?
```

## Notes

- The session analyzer script must be set up with a Python venv
- Tokens include input, output, and cache_read for total context usage
- Phase detection provides finer-grained categorization within long sessions
- This output is designed to be inserted into weekly review notes
