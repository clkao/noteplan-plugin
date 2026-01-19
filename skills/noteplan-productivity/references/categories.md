# Session Analysis Categories

## Category Definitions

### review
**Keywords:** weekly review, scan past due, checking progress, review, retrospective

**Description:** Sessions focused on reviewing completed work, checking progress against goals, or processing overdue items.

**Examples:**
- "weekly review"
- "scan past due tasks"
- "check my progress this week"
- "review Q1 goals"

### planning
**Keywords:** weekly plan, plan, priorities, scheduling, reprioritize, roadmap

**Description:** Sessions focused on planning future work, setting priorities, or scheduling tasks.

**Examples:**
- "weekly plan"
- "plan the week"
- "what should I prioritize?"
- "schedule my tasks"

### skill-dev
**Keywords:** skill, command, template, script, hook, agent, implement, create plugin

**Description:** Sessions focused on developing Claude Code skills, commands, hooks, or other productivity tooling.

**Examples:**
- "create a new skill"
- "update the weekly-review command"
- "add a hook for validation"
- "implement session analyzer"

### organization
**Keywords:** file inbox, filing, moving tasks, cleanup, organize, carry, archive

**Description:** Sessions focused on organizing notes, filing tasks, or general cleanup.

**Examples:**
- "file my inbox"
- "organize my tasks"
- "carry tasks to next week"
- "archive completed projects"

### content
**Keywords:** write, writing, notes, documentation, draft, document

**Description:** Sessions focused on writing content, documentation, or notes.

**Examples:**
- "write meeting notes"
- "draft documentation"
- "document this feature"
- "help me write..."

### coding
**Keywords:** code, fix, bug, test, debug, python, implement, script

**Description:** Sessions focused on writing or debugging code.

**Examples:**
- "fix this bug"
- "write a Python script"
- "debug the test failure"
- "implement the API endpoint"

### exploration
**Keywords:** what, how, where, find, search, understand, explore, explain

**Description:** Sessions focused on exploring, researching, or understanding something.

**Examples:**
- "what does this function do?"
- "how does the auth work?"
- "find all usages of X"
- "explain this code"

## Phase Detection

### Transition Signals

Detect phase transitions when user messages contain:

1. **Explicit transitions:**
   - "now let's..."
   - "moving on to..."
   - "next:"
   - "ok, let's..."

2. **Category keyword changes:**
   - Message classified differently than previous
   - New activity type begins

3. **Command triggers:**
   - "file inbox" (→ organization)
   - "weekly plan" (→ planning)
   - "weekly review" (→ review)

### Duration Calculation

Since per-message tokens aren't available:

1. Use message timestamps to calculate phase duration
2. Phase start = first message timestamp
3. Phase end = next phase start (or session end for last phase)
4. Allocate tokens proportionally by duration

### Example Phase Detection

Given messages:
```
1. "weekly review" at 10:00 → review
2. "carry tasks to W04" at 10:15 → review (same category)
3. "now let's update the skill" at 10:25 → skill-dev (TRANSITION)
4. "add error handling" at 10:35 → skill-dev (same)
5. "weekly plan" at 10:50 → planning (TRANSITION)
```

Detected phases:
- Phase 1: review (10:00-10:25, 25 min)
- Phase 2: skill-dev (10:25-10:50, 25 min)
- Phase 3: planning (10:50-end)

## Output Format

### Summary Table

```markdown
## Claude Code Usage

**Period:** 2026-W03 (Jan 13-19)
**Total time:** Xh Ym | **Tokens:** Nk

| Category     | Time    | Tokens  | Phases | Activities |
|--------------|---------|---------|--------|------------|
| review       | Xh Ym   | Nk      | N      | weekly review, scan overdue |
| skill-dev    | Xh Ym   | Nk      | N      | session analyzer, command updates |
| planning     | Xh Ym   | Nk      | N      | weekly plan |
| organization | Xh Ym   | Nk      | N      | file inbox |
```

### Session Breakdown

```markdown
**Session breakdown:**
- noteplan "weekly review" (1h 25m): review → skill-dev → planning
- noteplan "session analyzer" (50m): skill-dev
- recce-gtm "fix login bug" (30m): coding
```

### Notable Sessions

List top 3 sessions by duration:
```markdown
**Notable sessions:**
- `review` noteplan: "weekly review" - 1h 30m, 85k tokens
- `skill-dev` noteplan: "create session analyzer" - 1h 10m, 62k tokens
- `coding` recce-gtm: "implement API endpoint" - 45m, 38k tokens
```
