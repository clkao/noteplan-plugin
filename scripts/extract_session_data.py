#!/usr/bin/env python3
# ABOUTME: Extracts session metrics from Claude Code data files.
# ABOUTME: Run with --help for usage options.

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

CLAUDE_PROJECTS_DIR = Path.home() / '.claude' / 'projects'

def parse_week_arg(week_str):
    """Parse week argument like 'W03' or '2026-W03'."""
    match = re.match(r'^(?:(\d{4})-)?W(\d{2})$', week_str)
    if match:
        year = int(match.group(1)) if match.group(1) else datetime.now().year
        week = int(match.group(2))
        return year, week
    raise ValueError(f"Invalid week format: {week_str}. Use W03 or 2026-W03")

def get_week_date_range(year, week):
    """Return (start_date, end_date) for ISO week."""
    # Monday of the given week
    start = datetime.strptime(f'{year}-W{week:02d}-1', '%G-W%V-%u').date()
    # Sunday of the given week
    end = start + timedelta(days=6)
    return start, end


def find_sessions_indexes(projects_dir=None):
    """Find all sessions-index.json files in projects directory."""
    if projects_dir is None:
        projects_dir = CLAUDE_PROJECTS_DIR
    projects_dir = Path(projects_dir)
    return list(projects_dir.glob('*/sessions-index.json'))


def filter_sessions_by_date(sessions, start_date, end_date):
    """Filter sessions that were created within the date range."""
    result = []
    for session in sessions:
        created_str = session.get("created", "")
        if not created_str:
            continue
        # Parse ISO timestamp
        created = datetime.fromisoformat(created_str.replace("Z", "+00:00")).date()
        if start_date <= created <= end_date:
            result.append(session)
    return result


def extract_session_details(jsonl_path, max_user_messages=10):
    """Extract details from a session JSONL file."""
    user_messages = []
    timestamps = []
    total_input_tokens = 0
    total_output_tokens = 0
    total_cache_read = 0
    tool_call_count = 0
    message_count = 0
    messages_with_timestamps = []

    with open(jsonl_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            entry_type = entry.get("type")
            timestamp = entry.get("timestamp")

            if timestamp:
                timestamps.append(timestamp)

            if entry_type == "user":
                message_count += 1
                content = entry.get("message", {}).get("content", "")
                if isinstance(content, str) and content:
                    if len(user_messages) < max_user_messages:
                        user_messages.append(content)
                    # Always collect with timestamp for phase detection
                    messages_with_timestamps.append({
                        "content": content,
                        "timestamp": timestamp
                    })

            elif entry_type == "assistant":
                message_count += 1
                message = entry.get("message", {})
                usage = message.get("usage", {})

                total_input_tokens += usage.get("input_tokens", 0)
                total_output_tokens += usage.get("output_tokens", 0)
                total_cache_read += usage.get("cache_read_input_tokens", 0)

                # Count tool calls
                content = message.get("content", [])
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and item.get("type") == "tool_use":
                            tool_call_count += 1

    # Calculate duration
    duration_minutes = 0
    if len(timestamps) >= 2:
        timestamps.sort()
        first = datetime.fromisoformat(timestamps[0].replace("Z", "+00:00"))
        last = datetime.fromisoformat(timestamps[-1].replace("Z", "+00:00"))
        duration_minutes = int((last - first).total_seconds() / 60)

    return {
        "userMessages": user_messages,
        "messagesWithTimestamps": messages_with_timestamps,
        "duration_minutes": duration_minutes,
        "tokens": {
            "input": total_input_tokens,
            "output": total_output_tokens,
            "cache_read": total_cache_read
        },
        "messageCount": message_count,
        "toolCallCount": tool_call_count
    }


def extract_project_name(project_path):
    """Extract a short project name from the full path."""
    path = Path(project_path)
    name = path.name

    # Handle NotePlan app data directory special case
    # Only match the actual NotePlan app bundle path, not any dir with "noteplan" in name
    if "co.noteplan.NotePlan" in project_path:
        return "noteplan-data"

    return name


def process_sessions(projects_dir, start_date, end_date):
    """Process all sessions in date range, return structured data."""
    indexes = find_sessions_indexes(projects_dir)
    all_sessions = []

    for index_path in indexes:
        try:
            with open(index_path, 'r') as f:
                index_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            continue

        entries = index_data.get("entries", [])
        filtered = filter_sessions_by_date(entries, start_date, end_date)

        for entry in filtered:
            session_id = entry.get("sessionId", "")
            jsonl_path = index_path.parent / f"{session_id}.jsonl"

            if not jsonl_path.exists():
                continue

            details = extract_session_details(jsonl_path)

            session_data = {
                "id": session_id,
                "project": extract_project_name(entry.get("projectPath", "")),
                "firstPrompt": entry.get("firstPrompt", ""),
                "userMessages": details["userMessages"],
                "messagesWithTimestamps": details["messagesWithTimestamps"],
                "created": entry.get("created", ""),
                "modified": entry.get("modified", ""),
                "duration_minutes": details["duration_minutes"],
                "tokens": details["tokens"],
                "messageCount": entry.get("messageCount", details["messageCount"]),
                "toolCallCount": details["toolCallCount"]
            }
            all_sessions.append(session_data)

    # Sort by created time
    all_sessions.sort(key=lambda x: x.get("created", ""))

    return {
        "period": f"{start_date.isoformat()} to {end_date.isoformat()}",
        "sessions": all_sessions
    }


def main():
    parser = argparse.ArgumentParser(
        description='Extract session metrics from Claude Code data'
    )
    parser.add_argument(
        '--week', type=str,
        help='Week to analyze (W03 or 2026-W03). Defaults to current week.'
    )
    parser.add_argument(
        '--since', type=str,
        help='Start date (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--until', type=str,
        help='End date (YYYY-MM-DD)'
    )
    args = parser.parse_args()

    # Determine date range
    if args.since and args.until:
        start_date = datetime.strptime(args.since, '%Y-%m-%d').date()
        end_date = datetime.strptime(args.until, '%Y-%m-%d').date()
    elif args.week:
        year, week = parse_week_arg(args.week)
        start_date, end_date = get_week_date_range(year, week)
    else:
        # Default to current week
        today = datetime.now()
        year, week, _ = today.isocalendar()
        start_date, end_date = get_week_date_range(year, week)

    result = process_sessions(CLAUDE_PROJECTS_DIR, start_date, end_date)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
