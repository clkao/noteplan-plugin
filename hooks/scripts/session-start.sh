#!/bin/bash
# ABOUTME: SessionStart hook to detect NotePlan directory and inject context.
# ABOUTME: Outputs systemMessage for Claude if in NotePlan data directory.

# Check if we're in a NotePlan directory
if [[ -d "Calendar" && -d "Notes" ]] || [[ -f "CLAUDE.md" && $(grep -qi "noteplan" CLAUDE.md 2>/dev/null) ]]; then
    # Get day of week (1=Mon, 5=Fri)
    DOW=$(date +%u)

    if [[ "$DOW" == "1" ]]; then
        SUGGEST="Consider suggesting /noteplan:weekly-plan for Monday planning."
    elif [[ "$DOW" == "5" ]]; then
        SUGGEST="Consider suggesting /noteplan:weekly-review for Friday review."
    else
        SUGGEST="Available: /noteplan:file-inbox, /noteplan:scan-past-due, /noteplan:analyze-sessions."
    fi

    echo "{\"systemMessage\": \"NotePlan directory detected. $SUGGEST\"}"
fi

exit 0
