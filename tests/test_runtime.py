#!/usr/bin/env python3
"""Small end-to-end check for the public Codex plugin."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "ai-sloppy-copy"
SCRIPTS = PLUGIN / "scripts"
RULES = SCRIPTS / "AI-Sloppy-Copy-Rules.json"


def load_checker():
    spec = importlib.util.spec_from_file_location("ai_sloppy_copy", SCRIPTS / "ai_sloppy_copy.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["ai_sloppy_copy"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    hooks = json.loads((PLUGIN / "hooks/hooks.json").read_text(encoding="utf-8"))

    assert marketplace["name"] == "ai-sloppy-copy"
    assert marketplace["plugins"][0]["source"]["path"] == "./plugins/ai-sloppy-copy"
    assert manifest["name"] == "ai-sloppy-copy"
    assert manifest["version"] == "2.1.1"
    assert set(hooks["hooks"]) == {"UserPromptSubmit", "Stop"}

    checker = load_checker()
    rules = checker.load_rules(RULES)
    cases = json.loads((ROOT / "tests/cases.json").read_text(encoding="utf-8"))
    for case in cases:
        findings = checker.scan_text(case["text"], rules, source=case["id"])
        hard = [item for item in findings if item["enforcement"] == "hard"]
        rule_ids = {item["rule_id"] for item in findings}
        if case["expect"] == "fail":
            assert hard and any(rule.startswith(case["rule_id"]) for rule in rule_ids), case["id"]
        elif case["expect"] == "warning":
            assert case["rule_id"] in rule_ids and not hard, case["id"]
        else:
            assert not findings, case["id"]

    with tempfile.TemporaryDirectory() as folder:
        transcript = Path(folder) / "transcript.jsonl"
        transcript.write_text(
            json.dumps({"role": "assistant", "content": "We can leverage this process."}) + "\n",
            encoding="utf-8",
        )
        event = json.dumps(
            {
                "session_id": "public-runtime-test",
                "hook_event_name": "Stop",
                "transcript_path": str(transcript),
            }
        )
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "hook_ai_sloppy_copy.py")],
            input=event,
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        assert payload["continue"] is False
        assert "TERM-" in payload["stopReason"]

    public_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and path.suffix.lower() not in {".zip", ".pyc"}
    )
    forbidden = (
        "C:" + chr(92) + "Users" + chr(92),
        "aaron" + "@",
        "U08D9" + "BUMQ95",
        "90141" + "457186",
        "drjonesdc" + ".com",
    )
    assert not [value for value in forbidden if value.casefold() in public_text.casefold()]

    print(f"PASS: {len(cases)} cases, manifests, hooks, and public-data scan.")


if __name__ == "__main__":
    main()
