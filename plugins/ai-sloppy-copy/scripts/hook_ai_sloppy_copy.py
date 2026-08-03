#!/usr/bin/env python3
"""Claude Code and Codex hook adapter for the shared checker."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
from collections.abc import Iterator
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


def reversed_jsonl_lines(path: Path, block_size: int = 64 * 1024) -> Iterator[str]:
    """Yield complete JSONL lines newest first without reading the whole file."""
    with path.open("rb") as handle:
        handle.seek(0, os.SEEK_END)
        position = handle.tell()
        pending = b""
        while position:
            size = min(block_size, position)
            position -= size
            handle.seek(position)
            parts = (handle.read(size) + pending).split(b"\n")
            pending = parts[0]
            for line in reversed(parts[1:]):
                if line.strip():
                    yield line.decode("utf-8", errors="replace")
        if pending.strip():
            yield pending.decode("utf-8", errors="replace")


def last_codex_message(transcript_path: str | None) -> str:
    if not transcript_path:
        return ""
    path = Path(transcript_path)
    if not path.is_file():
        return ""
    for line in reversed_jsonl_lines(path):
        try:
            found = assistant_messages(json.loads(line))
        except json.JSONDecodeError:
            continue
        if found:
            return found[-1]
    return ""


def emit(value: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(value, ensure_ascii=False))


def repair_hints(findings: list[dict[str, Any]], limit: int = 5) -> str:
    """Return bounded repair context for the first two hook retries."""
    hints = []
    seen = set()
    for item in findings:
        rule_id = str(item.get("rule_id") or "")
        if not rule_id or rule_id in seen:
            continue
        seen.add(rule_id)
        match = " ".join(str(item.get("match") or "").split())[:80]
        action = " ".join(str(item.get("action") or "Rewrite the sentence.").split())[:180]
        hints.append(f"{rule_id} matched {json.dumps(match, ensure_ascii=False)}: {action}")
        if len(hints) == limit:
            break
    return " ".join(hints)


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    session_id = str(event.get("session_id") or event.get("sessionId") or os.getpid())
    event_name = str(event.get("hook_event_name") or event.get("hook_event") or "")
    if event_name == "UserPromptSubmit":
        reset_state(session_id)
        emit({})
        return 0
    if event_name and event_name != "Stop":
        emit({})
        return 0

    is_claude = "last_assistant_message" in event
    text = (
        str(event.get("last_assistant_message") or "")
        if is_claude
        else last_codex_message(event.get("transcript_path"))
    )
    if not text:
        emit({})
        return 0

    hard = [
        item
        for item in scan_text(text, load_rules(rules_path()), source="<assistant>")
        if item["enforcement"] == "hard"
    ]
    if not hard:
        reset_state(session_id)
        emit({})
        return 0

    rule_ids = ", ".join(sorted({item["rule_id"] for item in hard}))
    retry_message = (
        f"AI Sloppy Copy check failed. {repair_hints(hard)} "
        "Return the complete corrected deliverable only. Do not explain the repair, "
        "quote failed text, or return partial replacement instructions. Check again."
    )
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
                "reason": retry_message,
            }
        )
    else:
        emit(
            {
                "continue": False,
                "stopReason": retry_message,
                "systemMessage": retry_message,
            }
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
