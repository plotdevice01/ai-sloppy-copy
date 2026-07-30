# Changelog

## 2.2.4 - 2026-07-29

- Added a Claude Code marketplace and plugin manifest.
- Shared hooks now resolve both Codex and Claude Code plugin roots on Windows,
  macOS, and Linux.
- Restored the complete standalone writing contract inside the public skill so
  Claude Code does not depend on separate project instructions.
- Added Claude hook regression coverage and a dual-host release archive.

The Standard remains 2.1.1. No rule, evidence gate, voice gate, protected-text
boundary, or two-pass repair behavior was removed.

## 2.2.3 - 2026-07-29

- Excluded HTML and XML tag structure from prose rule scanning.
- Added regression coverage proving that an `align` attribute passes while
  prose using the blocked term still fails.
- Rules and evidence gates are unchanged. Voice gates, protected-text handling
  and lifecycle hooks are unchanged too.

## 2.2.2 - 2026-07-29

- Corrected the badge row after live GitHub rendering verification.
- Runtime rules and hooks are unchanged. Visual assets are also unchanged.

## 2.2.1 - 2026-07-29

- Updated GitHub Actions to the current Node.js 24-based releases.
- Runtime rules, hooks, documentation, and visual assets are unchanged.

## 2.2.0 - 2026-07-29

- Added a complete visual identity for the repository and Codex plugin.
- Rebuilt the README around proof and safe installation.
- Added workflow and boundary sections.
- Added local icon, logo, dark-mode logo, example, workflow, and social-preview
  assets.
- Added manifest presentation metadata and starter prompts.
- Added asset, accessibility, link, and portable-release parity checks.
- Expanded CI coverage to Python 3.10 through 3.13.
- Runtime rules and hook behavior are unchanged.

## 2.1.3 - 2026-07-29

- Completed the public documentation compliance pass.
- Runtime behavior is unchanged. Rules and hooks are unchanged.

## 2.1.2 - 2026-07-29

- Validated the public documentation against the bundled copy standard.
- Runtime behavior is unchanged. Rules and hooks are unchanged.

## 2.1.1 - 2026-07-29

- Made release archives byte-for-byte reproducible across Windows and Linux.
- Tightened public installation wording without changing rules or behavior.

## 2.1.0 - 2026-07-29

- Published the Codex marketplace and plugin as a public repository.
- Added Codex lifecycle hooks and the local standard-library checker.
- Added evidence, voice, protected-text, and authorship-claim controls.
- Validated 62 regression cases. Coverage includes 288 term rules. It also
  includes 21 expression rules and 34 style rules.
