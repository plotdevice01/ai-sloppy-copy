# Changelog

## 0.5.0 - 2026-08-03

### Changed

- Adopted one semantic product version. GitHub releases and tags now use the
  same version as both host manifests.
- Added a beginner-facing version guide to the public README. It explains the
  product package and the separate Standard rules contract.
- Strengthened hook repair feedback. Each retry must rescan the complete
  corrected answer instead of checking only the named passages.
- Accepted UTF-8 byte-order marks in hook JSON from Windows PowerShell.

### Validation

- Added the combined STYLE-001 and STYLE-008 review failure as a regression.
- Added coverage for a partial repair followed by a clean pass.
- Preserved 288 term rules and 21 expression rules. All 41 style rules remain.
  The nine paid-ad scenarios remain too.

### Compatibility

- Release, tag, ZIP, and host manifests use `0.5.0`.
- The package continues to include AI Sloppy Copy Standard `2.2.0`.

## 0.4 - 2026-08-02

### Added

- Added paid-ad mode for ad copy and creative on any advertising platform.
- Added the required Hook or Callout, Value, and Direct CTA structure.
- Added Problem and Promise, Mechanism and verified Proof, then Offer Snapshot
  and Risk as the ordered Value blocks.
- Added campaign CTA locking, three to five Value blocks, hook banks, and
  module-only output rules.
- Added evidence controls for offer facts, proof, testimonials, urgency,
  platform limits, and paid-media usage rights.
- Added a supplied-facts-only boundary for product behavior and delivery method.
  Automation and compatibility cannot be inferred. Workflow or customer-result
  claims also require supplied verification.
- Added a duration boundary. A call length cannot become a delivery time or a
  promised result unless that connection is supplied and verified.
- Added nine paid-ad acceptance scenarios, including the ad-spend reporting
  guard.
- Added bounded repair context to the first two Stop-hook retries. The message
  now includes the matched text plus its repair action. The third failure still
  returns rule IDs only.
- Removed the redundant Claude manifest hook declaration. Claude Code 2.1.140
  loads the standard hooks file automatically and reports the explicit entry as
  a duplicate.

### Compatibility

- Public release `0.4` contains AI Sloppy Copy Standard `2.2.0`.
- Codex and Claude Code manifests use `0.4.0`. The public release uses `0.4`.
  The Git tag matches it. Documentation and the ZIP use it too.

### Preserved

- All 288 term rules and 21 expression rules remain. The 34 existing style
  rules and 64 writing regression cases remain too.
- Protected-text controls remain. Evidence and voice gates remain, along with
  the hooks and two-pass repair limit.
- The stop hook remains deterministic. Context-dependent ad review stays in the
  skill instead of being reduced to unsafe text matching.

## 0.3 - 2026-07-30

### Changed

- Reset public release numbering from `2.2.6` to `0.3`. The project is still
  pre-1.0, and one-decimal milestones now communicate that status directly.
- `0.3` is the successor to `2.2.6` and fully contains it. The lower number is
  a numbering reset, not a rollback of code or rules. Capabilities remain.

### Compatibility

- Codex and Claude Code manifests use `0.3.0` because their plugin formats
  require strict three-part semantic versions. The public release uses `0.3`.
  The Git tag matches it. Documentation and the ZIP use it too.
- Existing `2.2.6` installations require one remove/reinstall cycle because
  semantic-version updaters sort `0.3.0` below `2.2.6`.

### Preserved

- All 288 term rules, 21 expression rules, 34 style rules and 64 regression
  cases.
- Evidence and voice gates, protected-text controls, the two-pass repair limit
  and Codex/Claude hooks.

## 2.2.6 - 2026-07-30

- Changed the Codex Stop hook to read JSONL transcripts from the end and stop
  at the newest assistant message instead of reparsing the full task history.
- Preserved Claude direct-message handling and every copy rule.
- Preserved the two-repair limit, state reset and Codex/Claude block responses.
- Added regression coverage for malformed trailing JSON; missing final
  newlines; block boundaries; and assistant messages larger than 64 KiB.

## 2.2.5 - 2026-07-29

- Fixed `--text` parsing on Python 3.10 and 3.11 by validating input modes
  after parsing instead of mixing an optional positional argument into an
  `argparse` exclusive group.
- Added a regression check for mixed text and file inputs.

No copy rule, evidence control, voice control or hook behavior changed.

## 2.2.4 - 2026-07-29

- Added a Claude Code marketplace and plugin manifest.
- Shared hooks now resolve both Codex and Claude Code plugin roots on Windows
  plus macOS/Linux.
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
