#!/usr/bin/env python3
"""Build a deterministic, installable marketplace ZIP."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "ai-sloppy-copy"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
MANIFEST_VERSION = f"{VERSION}.0"
NAME = f"AI-Sloppy-Copy-v{VERSION}"
OUTPUT = ROOT / "dist" / f"{NAME}.zip"
FILES = [
    ROOT / ".agents/plugins/marketplace.json",
    ROOT / ".claude-plugin/marketplace.json",
    ROOT / "VERSION",
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / "SECURITY.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "THIRD-PARTY-NOTICES.md",
    ROOT / "CHANGELOG.md",
    PLUGIN / ".codex-plugin/plugin.json",
    PLUGIN / ".claude-plugin/plugin.json",
    PLUGIN / "hooks/hooks.json",
    PLUGIN / "scripts/AI-Sloppy-Copy-Rules.json",
    PLUGIN / "scripts/ai_sloppy_copy.py",
    PLUGIN / "scripts/hook_ai_sloppy_copy.py",
    PLUGIN / "skills/ai-sloppy-copy/SKILL.md",
    PLUGIN / "skills/ai-sloppy-copy/agents/openai.yaml",
] + sorted(path for path in (PLUGIN / "assets").iterdir() if path.is_file())


def build(output: Path = OUTPUT) -> str:
    manifest_version = json.loads(
        (PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
    )["version"]
    if manifest_version != MANIFEST_VERSION:
        raise RuntimeError(
            f"Plugin manifest is {manifest_version}; expected {MANIFEST_VERSION}."
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for path in FILES:
            relative = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(f"{NAME}/{relative}", (2026, 8, 2, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, path.read_bytes().replace(b"\r\n", b"\n"))
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"{output}\nSHA-256: {digest}")
    return digest


if __name__ == "__main__":
    build()
