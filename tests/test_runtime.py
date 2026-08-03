#!/usr/bin/env python3
"""Small end-to-end check for the public Codex plugin."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "ai-sloppy-copy"
SCRIPTS = PLUGIN / "scripts"
RULES = SCRIPTS / "AI-Sloppy-Copy-Rules.json"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
MANIFEST_VERSION = VERSION


def load_checker():
    spec = importlib.util.spec_from_file_location("ai_sloppy_copy", SCRIPTS / "ai_sloppy_copy.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["ai_sloppy_copy"] = module
    spec.loader.exec_module(module)
    return module


def load_hook():
    spec = importlib.util.spec_from_file_location(
        "hook_ai_sloppy_copy", SCRIPTS / "hook_ai_sloppy_copy.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["hook_ai_sloppy_copy"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    claude_marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    claude_manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    hooks = json.loads((PLUGIN / "hooks/hooks.json").read_text(encoding="utf-8"))

    assert marketplace["name"] == "ai-sloppy-copy"
    assert marketplace["plugins"][0]["source"]["path"] == "./plugins/ai-sloppy-copy"
    assert manifest["name"] == "ai-sloppy-copy"
    assert VERSION == "0.5.0"
    assert manifest["version"] == MANIFEST_VERSION
    assert claude_marketplace["name"] == "ai-sloppy-copy"
    assert claude_marketplace["plugins"][0]["source"] == "./plugins/ai-sloppy-copy"
    assert claude_manifest["name"] == "ai-sloppy-copy"
    assert claude_manifest["version"] == manifest["version"]
    assert "hooks" not in claude_manifest
    assert set(hooks["hooks"]) == {"UserPromptSubmit", "Stop"}
    for event in hooks["hooks"].values():
        command = event[0]["hooks"][0]["commandWindows"]
        command_unix = event[0]["hooks"][0]["command"]
        assert "$env:PLUGIN_ROOT" in command and "$env:CLAUDE_PLUGIN_ROOT" in command
        assert "PLUGIN_ROOT" in command_unix and "CLAUDE_PLUGIN_ROOT" in command_unix
        assert "%PLUGIN_ROOT%" not in command

    interface = manifest["interface"]
    asset_paths = [
        interface["composerIcon"],
        interface["logo"],
        interface["logoDark"],
        *interface["screenshots"],
    ]
    for relative in asset_paths:
        asset = PLUGIN / relative.removeprefix("./")
        assert asset.is_file(), relative
        assert asset.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), relative

    svg_assets = sorted((PLUGIN / "assets").glob("*.svg"))
    assert svg_assets
    for asset in svg_assets:
        root = ET.parse(asset).getroot()
        namespace = {"svg": "http://www.w3.org/2000/svg"}
        assert root.find("svg:title", namespace) is not None, asset.name
        assert root.find("svg:desc", namespace) is not None, asset.name

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Versions explained" in readme
    assert "0.5.0" in readme
    assert "Standard `2.2.0`" in readme
    local_references = re.findall(r"\]\((?!https?://|#)([^)]+)\)", readme)
    local_references += re.findall(r'(?:src|srcset)="(?!https?://)([^"]+)"', readme)
    for relative in local_references:
        assert (ROOT / relative).is_file(), relative

    checker = load_checker()
    hook = load_hook()
    rules = checker.load_rules(RULES)
    assert rules["standard"]["version"] == "2.2.0"
    ad_rules = [item for item in rules["style_rules"] if item["rule_id"].startswith("ADS-")]
    assert [item["rule_id"] for item in ad_rules] == [f"ADS-{number:03d}" for number in range(1, 8)]
    assert all(item["reviewer_only"] and item["enforcement"] == "review" for item in ad_rules)
    ad_cases = json.loads((ROOT / "tests/ad-framework-cases.json").read_text(encoding="utf-8"))
    assert len(ad_cases) == 9
    disabled_ad_cases = [case for case in ad_cases if not case["activate_paid_ad_mode"]]
    assert [case["id"] for case in disabled_ad_cases] == ["SPEND-REPORT"]
    skill_text = (PLUGIN / "skills/ai-sloppy-copy/SKILL.md").read_text(encoding="utf-8")
    skill_flat = " ".join(skill_text.split())
    for required in (
        "## Paid ad mode",
        "Hook or Callout",
        "keep one CTA fixed",
        "three to five Value blocks",
        "only mentions ads or ad spend",
        "paid-media usage rights",
    ):
        assert required in skill_flat, required
    cli_fail = subprocess.run(
        [sys.executable, str(SCRIPTS / "ai_sloppy_copy.py"), "--text", "We need to align the stakeholders."],
        text=True,
        capture_output=True,
    )
    assert cli_fail.returncode == 1 and "TERM-032" in cli_fail.stdout
    cli_invalid = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "ai_sloppy_copy.py"),
            "--text",
            "Draft",
            str(ROOT / "README.md"),
        ],
        text=True,
        capture_output=True,
    )
    assert cli_invalid.returncode != 0 and "either --text" in cli_invalid.stderr
    cli_pass = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "ai_sloppy_copy.py"),
            "--text",
            '<p align="center">The report is ready.</p>',
        ],
        text=True,
        capture_output=True,
    )
    assert cli_pass.returncode == 0 and "PASS: no AI Sloppy Copy findings." in cli_pass.stdout
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
        reset = subprocess.run(
            [sys.executable, str(SCRIPTS / "hook_ai_sloppy_copy.py")],
            input=json.dumps(
                {
                    "session_id": "public-runtime-test",
                    "hook_event_name": "UserPromptSubmit",
                }
            ),
            text=True,
            capture_output=True,
            check=True,
        )
        assert json.loads(reset.stdout) == {}
        bom_reset = subprocess.run(
            [sys.executable, str(SCRIPTS / "hook_ai_sloppy_copy.py")],
            input="\ufeff"
            + json.dumps(
                {
                    "session_id": "public-runtime-bom-test",
                    "hook_event_name": "UserPromptSubmit",
                }
            ),
            text=True,
            capture_output=True,
            check=True,
        )
        assert json.loads(bom_reset.stdout) == {}
        transcript = Path(folder) / "transcript.jsonl"
        large = "x" * 70000 + " latest assistant message"
        transcript.write_text(
            "\n".join(
                [
                    json.dumps({"role": "assistant", "content": "old"}),
                    json.dumps({"role": "user", "content": "new prompt"}),
                    json.dumps({"role": "assistant", "content": large}),
                    '{"malformed":',
                ]
            ),
            encoding="utf-8",
        )
        assert hook.last_codex_message(str(transcript)) == large
        reverse_fixture = Path(folder) / "reverse.jsonl"
        reverse_fixture.write_bytes(b"first\nsecond\nthird")
        assert list(hook.reversed_jsonl_lines(reverse_fixture, block_size=4)) == [
            "third",
            "second",
            "first",
        ]

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

        claude_session = "public-claude-runtime-test"
        claude_reset = subprocess.run(
            [sys.executable, str(SCRIPTS / "hook_ai_sloppy_copy.py")],
            input=json.dumps(
                {
                    "session_id": claude_session,
                    "hook_event_name": "UserPromptSubmit",
                }
            ),
            text=True,
            capture_output=True,
            check=True,
        )
        assert json.loads(claude_reset.stdout) == {}
        claude = subprocess.run(
            [sys.executable, str(SCRIPTS / "hook_ai_sloppy_copy.py")],
            input=json.dumps(
                {
                    "session_id": claude_session,
                    "hook_event_name": "Stop",
                    "last_assistant_message": "We can leverage this process.",
                }
            ),
            text=True,
            capture_output=True,
            check=True,
        )
        claude_payload = json.loads(claude.stdout)
        assert claude_payload["decision"] == "block"
        assert "TERM-" in claude_payload["reason"]
        assert 'matched "leverage"' in claude_payload["reason"]
        assert "concrete information" in claude_payload["reason"]
        assert "complete corrected deliverable only" in claude_payload["reason"]

        repair_session = "public-repair-runtime-test"
        subprocess.run(
            [sys.executable, str(SCRIPTS / "hook_ai_sloppy_copy.py")],
            input=json.dumps(
                {
                    "session_id": repair_session,
                    "hook_event_name": "UserPromptSubmit",
                }
            ),
            text=True,
            capture_output=True,
            check=True,
        )
        first_repair = subprocess.run(
            [sys.executable, str(SCRIPTS / "hook_ai_sloppy_copy.py")],
            input=json.dumps(
                {
                    "session_id": repair_session,
                    "hook_event_name": "Stop",
                    "last_assistant_message": (
                        "Product release 0.4\u2014The package includes the checker, "
                        "Codex and Claude manifests, and supporting assets. The Standard "
                        "covers protected-text behavior, paid-ad requirements, and "
                        "enforcement expectations."
                    ),
                }
            ),
            text=True,
            capture_output=True,
            check=True,
        )
        first_repair_payload = json.loads(first_repair.stdout)
        assert first_repair_payload["decision"] == "block"
        assert "STYLE-001" in first_repair_payload["reason"]
        assert "STYLE-008" in first_repair_payload["reason"]
        assert "full corrected deliverable again" in first_repair_payload["reason"]

        second_repair = subprocess.run(
            [sys.executable, str(SCRIPTS / "hook_ai_sloppy_copy.py")],
            input=json.dumps(
                {
                    "session_id": repair_session,
                    "hook_event_name": "Stop",
                    "last_assistant_message": (
                        "The package includes the checker, both host manifests, and visual "
                        "assets. The Standard covers protected-text behavior, paid-ad "
                        "requirements, and enforcement expectations."
                    ),
                }
            ),
            text=True,
            capture_output=True,
            check=True,
        )
        second_repair_payload = json.loads(second_repair.stdout)
        assert second_repair_payload["decision"] == "block"
        assert "STYLE-008" in second_repair_payload["reason"]

        repaired = subprocess.run(
            [sys.executable, str(SCRIPTS / "hook_ai_sloppy_copy.py")],
            input=json.dumps(
                {
                    "session_id": repair_session,
                    "hook_event_name": "Stop",
                    "last_assistant_message": (
                        "The package includes the checker and both host manifests. Visual "
                        "assets are included. The Standard defines protected-text behavior "
                        "plus paid-ad requirements. It also defines enforcement expectations."
                    ),
                }
            ),
            text=True,
            capture_output=True,
            check=True,
        )
        assert json.loads(repaired.stdout) == {}

    public_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() not in {".zip", ".pyc", ".png"}
    )
    forbidden = (
        "C:" + chr(92) + "Users" + chr(92),
        "aaron" + "@",
        "U08D9" + "BUMQ95",
        "90141" + "457186",
        "drjonesdc" + ".com",
    )
    assert not [value for value in forbidden if value.casefold() in public_text.casefold()]

    print(
        f"PASS: {len(cases)} writing cases and {len(ad_cases)} paid-ad scenarios, "
        "manifests, hooks, and public-data scan."
    )


if __name__ == "__main__":
    main()
