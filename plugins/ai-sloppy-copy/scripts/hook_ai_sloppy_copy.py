#!/usr/bin/env python3
"""Claude Code and Codex hook adapter for the shared checker."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from ai_sloppy_copy import load_rules, scan_text


def rules_path() -> Path:
    local = Path(__file__).resolve().parent / "AI-Sloppy-Copy-Rules.json"
    if local.exists():
        return local
    return Path(__file__).resolve().parent.parent / "dist" / "AI-Sloppy-Copy-Rules.json"


def state_path(session_id: str) -> Path:
    key = hashlib.sha256(session_id.encode("utf-8")).hexdigest()
    root = Path(tempfile.gettempdir()) / "ai-sloppy-copy-hook-state"
    root.mkdir(parents=True, exist_ok=True)
    return root / f"{key}.json"


def reset_state(session_id: str) -> None:
    path = state_path(session_id)
    if path.exists():
        path.unlink()


def next_failure(session_id: str) -> int:
    path = state_path(session_id)
    count = 0
    if path.exists():
        try:
            count = int(json.loads(path.read_text(encoding="utf-8")).get("failures", 0))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            count = 0
    count += 1
    path.write_text(json.dumps({"failures": count}), encoding="utf-8")
    return count


def content_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        values = []
        for item in content:
            if isinstance(item, str):
                values.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                values.append(item["text"])
        return "\n".join(values)
    return ""


def assistant_messages(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        if value.get("role") == "assistant":
            text = content_text(value.get("content"))
            if not text and isinstance(value.get("text"), str):
                text = value["text"]
            if text:
                found.append(text)
        for child in value.values():
            found.extend(assistant_messages(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(assistant_messages(child))
    return found


def last_codex_message(transcript_path: str | None) -> str:
    if not transcript_path:
        return ""
    path = Path(transcript_path)
    if not path.is_file():
        return ""
    found: list[str] = []
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                found.extend(assistant_messages(json.loads(line)))
            except json.JSONDecodeError:
                continue
    return found[-1] if found else ""


def emit(value: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(value, ensure_ascii=False))


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    session_id = str(event.get("session_id") or event.get("sessionId") or os.getpid())
    event_name = str(event.get("hook_event_name") or event.get("hook_event") or "")
    if event_name == "UserPromptSubmit":
        reset_state(session_id)
        return 0
    if event_name and event_name != "Stop":
        return 0

    is_claude = "last_assistant_message" in event
    text = (
        str(event.get("last_assistant_message") or "")
        if is_claude
        else last_codex_message(event.get("transcript_path"))
    )
    if not text:
        return 0

    hard = [
        item
        for item in scan_text(text, load_rules(rules_path()), source="<assistant>")
        if item["enforcement"] == "hard"
    ]
    if not hard:
        reset_state(session_id)
        return 0

    rule_ids = ", ".join(sorted({item["rule_id"] for item in hard}))
    failure = next_failure(session_id)
    if failure > 2 and is_claude:
        emit(
            {
                "decision": "block",
                "reason": f"Draft withheld. Return only this text: Failed rules: {rule_ids}",
            }
        )
    elif failure > 2:
        emit(
            {
                "continue": False,
                "stopReason": f"Draft withheld. Failed rules: {rule_ids}",
                "systemMessage": f"Draft withheld. Failed rules: {rule_ids}",
            }
        )
    elif is_claude:
        emit(
            {
                "decision": "block",
                "reason": f"AI Sloppy Copy check failed: {rule_ids}. Rewrite and check again.",
            }
        )
    else:
        emit(
            {
                "continue": False,
                "stopReason": f"AI Sloppy Copy check failed: {rule_ids}. Rewrite and check again.",
                "systemMessage": f"AI Sloppy Copy check failed: {rule_ids}. Rewrite and check again.",
            }
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
