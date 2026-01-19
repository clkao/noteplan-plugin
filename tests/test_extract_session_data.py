#!/usr/bin/env python3
# ABOUTME: Tests for extract_session_data.py script.
# ABOUTME: Uses pytest for testing session data extraction.

import json
import pytest
from datetime import datetime, date
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from extract_session_data import parse_week_arg, get_week_date_range

def test_parse_week_arg_with_week_format():
    """Parse W03 or 2026-W03 format."""
    year, week = parse_week_arg("W03")
    # Should use current year
    assert week == 3

    year, week = parse_week_arg("2026-W03")
    assert year == 2026
    assert week == 3

def test_get_week_date_range():
    """Get start/end dates for a week."""
    start, end = get_week_date_range(2026, 3)
    # ISO week 3 of 2026: Monday Jan 12 to Sunday Jan 18
    assert start.isoformat() == "2026-01-12"
    assert end.isoformat() == "2026-01-18"


def test_find_sessions_indexes(tmp_path):
    """Find all sessions-index.json files in projects directory."""
    from extract_session_data import find_sessions_indexes

    # Create mock project directories
    proj1 = tmp_path / "project1"
    proj1.mkdir()
    (proj1 / "sessions-index.json").write_text('{"version":1,"entries":[]}')

    proj2 = tmp_path / "project2"
    proj2.mkdir()
    (proj2 / "sessions-index.json").write_text('{"version":1,"entries":[]}')

    indexes = find_sessions_indexes(tmp_path)
    assert len(indexes) == 2
    assert all(p.name == "sessions-index.json" for p in indexes)


def test_filter_sessions_by_date():
    """Filter sessions that fall within a date range."""
    from extract_session_data import filter_sessions_by_date

    sessions = [
        {"sessionId": "1", "created": "2026-01-13T10:00:00Z", "modified": "2026-01-13T11:00:00Z"},
        {"sessionId": "2", "created": "2026-01-15T10:00:00Z", "modified": "2026-01-15T11:00:00Z"},
        {"sessionId": "3", "created": "2026-01-20T10:00:00Z", "modified": "2026-01-20T11:00:00Z"},
    ]

    start = date(2026, 1, 13)
    end = date(2026, 1, 19)

    filtered = filter_sessions_by_date(sessions, start, end)
    assert len(filtered) == 2
    assert filtered[0]["sessionId"] == "1"
    assert filtered[1]["sessionId"] == "2"


def test_extract_user_messages(tmp_path):
    """Extract user message content from JSONL file."""
    from extract_session_data import extract_session_details

    jsonl_file = tmp_path / "test-session.jsonl"
    lines = [
        json.dumps({"type": "user", "message": {"role": "user", "content": "weekly review"}, "timestamp": "2026-01-19T10:00:00Z"}),
        json.dumps({"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": "Starting..."}]}, "timestamp": "2026-01-19T10:00:05Z"}),
        json.dumps({"type": "user", "message": {"role": "user", "content": "carry to W04"}, "timestamp": "2026-01-19T10:01:00Z"}),
    ]
    jsonl_file.write_text("\n".join(lines))

    details = extract_session_details(jsonl_file, max_user_messages=5)

    assert details["userMessages"] == ["weekly review", "carry to W04"]


def test_extract_token_usage(tmp_path):
    """Extract and sum token usage from assistant messages."""
    from extract_session_data import extract_session_details

    jsonl_file = tmp_path / "test-session.jsonl"
    lines = [
        json.dumps({
            "type": "user",
            "message": {"role": "user", "content": "hello"},
            "timestamp": "2026-01-19T10:00:00Z"
        }),
        json.dumps({
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [{"type": "text", "text": "Hi there!"}],
                "usage": {
                    "input_tokens": 100,
                    "output_tokens": 50,
                    "cache_read_input_tokens": 20
                }
            },
            "timestamp": "2026-01-19T10:00:05Z"
        }),
        json.dumps({
            "type": "user",
            "message": {"role": "user", "content": "thanks"},
            "timestamp": "2026-01-19T10:01:00Z"
        }),
        json.dumps({
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [{"type": "text", "text": "You're welcome!"}],
                "usage": {
                    "input_tokens": 200,
                    "output_tokens": 30,
                    "cache_read_input_tokens": 80
                }
            },
            "timestamp": "2026-01-19T10:01:05Z"
        }),
    ]
    jsonl_file.write_text("\n".join(lines))

    details = extract_session_details(jsonl_file)

    assert details["tokens"]["input"] == 300  # 100 + 200
    assert details["tokens"]["output"] == 80  # 50 + 30
    assert details["tokens"]["cache_read"] == 100  # 20 + 80


def test_extract_duration(tmp_path):
    """Extract duration in minutes from first to last timestamp."""
    from extract_session_data import extract_session_details

    jsonl_file = tmp_path / "test-session.jsonl"
    # Session spanning 10:00 to 11:03 = 63 minutes
    lines = [
        json.dumps({
            "type": "user",
            "message": {"role": "user", "content": "start task"},
            "timestamp": "2026-01-19T10:00:00Z"
        }),
        json.dumps({
            "type": "assistant",
            "message": {"role": "assistant", "content": [{"type": "text", "text": "Working..."}]},
            "timestamp": "2026-01-19T10:30:00Z"
        }),
        json.dumps({
            "type": "user",
            "message": {"role": "user", "content": "done"},
            "timestamp": "2026-01-19T11:03:00Z"
        }),
    ]
    jsonl_file.write_text("\n".join(lines))

    details = extract_session_details(jsonl_file)

    assert details["duration_minutes"] == 63


def test_extract_tool_call_count(tmp_path):
    """Extract and count tool_use content blocks from assistant messages."""
    from extract_session_data import extract_session_details

    jsonl_file = tmp_path / "test-session.jsonl"
    lines = [
        json.dumps({
            "type": "user",
            "message": {"role": "user", "content": "read the file"},
            "timestamp": "2026-01-19T10:00:00Z"
        }),
        json.dumps({
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [
                    {"type": "tool_use", "id": "tool1", "name": "Read", "input": {"file_path": "/tmp/test.py"}},
                    {"type": "text", "text": "Let me read the file."}
                ]
            },
            "timestamp": "2026-01-19T10:00:05Z"
        }),
        json.dumps({
            "type": "user",
            "message": {"role": "user", "content": "now edit it"},
            "timestamp": "2026-01-19T10:01:00Z"
        }),
        json.dumps({
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [
                    {"type": "tool_use", "id": "tool2", "name": "Edit", "input": {"file_path": "/tmp/test.py", "old_string": "a", "new_string": "b"}},
                    {"type": "tool_use", "id": "tool3", "name": "Bash", "input": {"command": "python /tmp/test.py"}}
                ]
            },
            "timestamp": "2026-01-19T10:01:05Z"
        }),
    ]
    jsonl_file.write_text("\n".join(lines))

    details = extract_session_details(jsonl_file)

    # 1 tool_use in first assistant message + 2 tool_use in second = 3 total
    assert details["toolCallCount"] == 3


def test_extract_project_name():
    """Extract short project name from projectPath."""
    from extract_session_data import extract_project_name

    # NotePlan app data directory gets special name
    path = "/Users/clkao/Library/Containers/co.noteplan.NotePlan3/Data/Library/Application Support/co.noteplan.NotePlan3"
    assert extract_project_name(path) == "noteplan-data"

    # Regular git repos use directory name
    path2 = "/Users/clkao/git/recce-gtm"
    assert extract_project_name(path2) == "recce-gtm"

    path3 = "/Users/clkao/git/clipa-ledger"
    assert extract_project_name(path3) == "clipa-ledger"

    # noteplan-plugin should NOT be shortened to "noteplan"
    path4 = "/Users/clkao/git/noteplan-plugin"
    assert extract_project_name(path4) == "noteplan-plugin"


def test_process_sessions(tmp_path):
    """Process sessions from index and extract details."""
    from extract_session_data import process_sessions

    # Create mock project
    proj = tmp_path / "project1"
    proj.mkdir()

    # Create sessions index
    index = {
        "version": 1,
        "entries": [
            {
                "sessionId": "abc123",
                "firstPrompt": "weekly review",
                "messageCount": 10,
                "created": "2026-01-15T10:00:00Z",
                "modified": "2026-01-15T11:00:00Z",
                "projectPath": "/Users/test/git/myproject"
            }
        ]
    }
    (proj / "sessions-index.json").write_text(json.dumps(index))

    # Create JSONL file
    jsonl_lines = [
        json.dumps({"type": "user", "message": {"content": "weekly review"}, "timestamp": "2026-01-15T10:00:00Z"}),
        json.dumps({"type": "assistant", "message": {"usage": {"input_tokens": 100, "output_tokens": 50, "cache_read_input_tokens": 0}}, "timestamp": "2026-01-15T11:00:00Z"}),
    ]
    (proj / "abc123.jsonl").write_text("\n".join(jsonl_lines))

    # Process
    start = date(2026, 1, 13)
    end = date(2026, 1, 19)
    result = process_sessions(tmp_path, start, end)

    assert result["period"] == "2026-01-13 to 2026-01-19"
    assert len(result["sessions"]) == 1
    assert result["sessions"][0]["id"] == "abc123"
    assert result["sessions"][0]["project"] == "myproject"
    assert result["sessions"][0]["firstPrompt"] == "weekly review"
    assert "messagesWithTimestamps" in result["sessions"][0]
    assert len(result["sessions"][0]["messagesWithTimestamps"]) == 1
    assert result["sessions"][0]["messagesWithTimestamps"][0]["content"] == "weekly review"


def test_extract_messages_with_timestamps(tmp_path):
    """Extract user messages with their timestamps."""
    from extract_session_data import extract_session_details

    jsonl_file = tmp_path / "test-session.jsonl"
    lines = [
        json.dumps({"type": "user", "message": {"content": "weekly review"}, "timestamp": "2026-01-19T10:00:00Z"}),
        json.dumps({"type": "assistant", "message": {"content": []}, "timestamp": "2026-01-19T10:05:00Z"}),
        json.dumps({"type": "user", "message": {"content": "now let's plan"}, "timestamp": "2026-01-19T10:20:00Z"}),
        json.dumps({"type": "assistant", "message": {"content": []}, "timestamp": "2026-01-19T10:25:00Z"}),
        json.dumps({"type": "user", "message": {"content": "file inbox"}, "timestamp": "2026-01-19T10:40:00Z"}),
    ]
    jsonl_file.write_text("\n".join(lines))

    details = extract_session_details(jsonl_file)

    assert "messagesWithTimestamps" in details
    assert len(details["messagesWithTimestamps"]) == 3
    assert details["messagesWithTimestamps"][0]["content"] == "weekly review"
    assert details["messagesWithTimestamps"][0]["timestamp"] == "2026-01-19T10:00:00Z"
    assert details["messagesWithTimestamps"][1]["content"] == "now let's plan"
    assert details["messagesWithTimestamps"][1]["timestamp"] == "2026-01-19T10:20:00Z"
    assert details["messagesWithTimestamps"][2]["content"] == "file inbox"
    assert details["messagesWithTimestamps"][2]["timestamp"] == "2026-01-19T10:40:00Z"
