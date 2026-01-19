#!/bin/bash
# ABOUTME: SessionStart hook to detect NotePlan directory and show available workflows.
# ABOUTME: Outputs a reminder message if in NotePlan data directory.

# Check if we're in a NotePlan directory
if [[ -d "Calendar" && -d "Notes" ]] || [[ -f "CLAUDE.md" && $(grep -qi "noteplan" CLAUDE.md 2>/dev/null) ]]; then
    echo "NotePlan directory detected. Available workflows:"
    echo "- /noteplan:weekly-plan (Monday planning)"
    echo "- /noteplan:weekly-review (Friday review)"
    echo "- /noteplan:file-inbox (file unfiled tasks)"
    echo "- /noteplan:scan-past-due (find overdue)"
    echo "- /noteplan:analyze-sessions (Claude usage)"
fi

exit 0
