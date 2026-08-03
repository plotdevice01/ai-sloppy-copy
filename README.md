<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="plugins/ai-sloppy-copy/assets/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="plugins/ai-sloppy-copy/assets/logo.svg">
    <img alt="AI Sloppy Copy: Evidence-backed copy. Local rule enforcement." src="plugins/ai-sloppy-copy/assets/logo.svg" width="900">
  </picture>
</h1>

<p align="center">
  Copy and paid-ad guardrails for Codex and Claude Code: verify the claim,
  protect exact text, match the approved voice, and stop blocked phrasing.
</p>

<p align="center"><a href="https://github.com/plotdevice01/ai-sloppy-copy/actions/workflows/validate.yml"><img alt="CI status" src="https://github.com/plotdevice01/ai-sloppy-copy/actions/workflows/validate.yml/badge.svg"></a> <a href="https://github.com/plotdevice01/ai-sloppy-copy/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/plotdevice01/ai-sloppy-copy"></a> <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-0f766e.svg"></a> <img alt="Codex and Claude Code" src="https://img.shields.io/badge/hosts-Codex_%2B_Claude_Code-0f766e.svg"> <img alt="Python standard library" src="https://img.shields.io/badge/Python-stdlib_only-3776AB.svg"> <img alt="Local checker with no telemetry" src="https://img.shields.io/badge/checker-local_only-14b8a6.svg"></p>

<p align="center">
  <a href="#install">Install</a> |
  <a href="#see-it-work">Example</a> |
  <a href="#versions-explained">Versions</a> |
  <a href="#what-it-enforces">Rules</a> |
  <a href="#use-the-checker-directly">CLI</a> |
  <a href="#privacy-and-security">Security</a>
</p>

AI Sloppy Copy is a Codex and Claude Code plugin with a deterministic local
checker. It catches prohibited model-written patterns, applies evidence and
voice controls, preserves paid-ad structure, and returns exact rule IDs for
repair. The operator keeps final approval.

It does **not** identify who wrote text or promise AI-detector results. Rule
compliance and authorship are different questions.

## What changed in v0.5.0

- The GitHub release, tag, ZIP, and both host manifests now use `0.5.0`.
- Windows PowerShell hook input may begin with a UTF-8 byte-order mark. The
  parser now accepts it instead of silently skipping the event.
- The combined STYLE-001 and STYLE-008 failure shown during the `0.4.0` review
  is now a regression case. The test covers a partial repair plus a clean pass.
- Repair feedback now requires another scan of the complete corrected answer.
  Checking only the named passages is not enough.
- Paid-ad behavior remains unchanged. Standard `2.2.0` remains the active
  rules contract.

## Versions explained

AI Sloppy Copy has one product version and one Standard version. Users install
and cite the product version.

| Layer | Current version | What it identifies | When it changes |
| --- | ---: | --- | --- |
| Product | `0.5.0` | The GitHub release and installable ZIP. Both host manifests carry the same number. | Plugin code, hooks, packaging, or public documentation changes. |
| Standard | `2.2.0` | The rules contract used by the skill and local checker. | A writing rule or its enforcement contract changes. |

The product package contains the skill instructions and lifecycle hooks. It
also carries the local checker with its compiled rules. Host manifests and
visual assets are included.

Standard `2.2.0` defines 288 term rules plus 21 expression rules. It defines 41
style rules too. Evidence controls and approved-voice boundaries are part of
the contract. Protected-text handling and paid-ad requirements are included.

A manifest is a small JSON file inside the plugin. Codex and Claude Code read
it to identify the plugin plus its version. The Codex manifest also identifies
the skill location and interface assets. A manifest is not a separate release.

## See it work

![A generic draft is flagged and repaired with specific language.](plugins/ai-sloppy-copy/assets/before-after.svg)

```text
Input
We can leverage this cutting-edge system to turbocharge production.

Hard failures
TERM-021  leverage
TERM-007  cutting-edge
TERM-211  turbocharge

Repair
Run the local checker before publishing. It flags blocked phrases and returns
rule IDs for repair.
```

The checker reports the problem. It does not perform reckless global
replacement or silently change protected text.

## What it enforces

| Control | Result |
| --- | --- |
| Evidence gates | Unsupported recommendations, testimonials, case studies, and claims require a verified basis. |
| Paid-ad structure | Complete ads preserve a Hook or Callout. They also preserve ordered Value plus one Direct CTA. |
| Campaign controls | One CTA stays fixed while hooks and three to five Value blocks are tested. |
| Approved voice | Named-person copy requires owner-approved voice samples. |
| Protected text | Quotes, code, commands, paths, IDs, legal text, and required vendor wording stay exact. |
| Hard rules | Banned terms and prohibited expressions block release. |
| Review rules | Context-dependent style flags stay visible for human judgment. |
| Authorship boundary | Compliance is never presented as proof of human authorship. |

| Included coverage | Count |
| --- | ---: |
| Term rules | 288 |
| Expression rules | 21 |
| Style rules | 41 |
| Regression cases | 67 |
| Paid-ad scenarios | 9 |
| Checker network calls | 0 |

## Install

You need [Python 3](https://www.python.org/downloads/) plus
[Codex](https://developers.openai.com/codex/) or
[Claude Code](https://code.claude.com/docs/en/setup). No repository clone is
required. No local path or checksum ceremony is required.

### Codex

Open a terminal. Windows users can use PowerShell or the Codex terminal. Run
each command once:

```powershell
codex plugin marketplace add plotdevice01/ai-sloppy-copy
codex plugin add ai-sloppy-copy@ai-sloppy-copy
```

If Codex says the marketplace already exists, update it:

```powershell
codex plugin marketplace upgrade ai-sloppy-copy
```

If you still have a legacy `2.2.6` installation, reinstall once.
Semantic-version updaters correctly but unhelpfully sort `0.5.0` below
`2.2.6`:

```powershell
codex plugin remove ai-sloppy-copy
codex plugin marketplace upgrade ai-sloppy-copy
codex plugin add ai-sloppy-copy@ai-sloppy-copy
```

Restart Codex, open `/hooks`, review `UserPromptSubmit` and `Stop`, and start a
fresh task. Confirm the plugin:

```powershell
codex plugin list --json
```

### Claude Code

```powershell
claude plugin marketplace add plotdevice01/ai-sloppy-copy
claude plugin install ai-sloppy-copy@ai-sloppy-copy --scope user
```

If you still have a legacy `2.2.6` installation, reinstall once:

```powershell
claude plugin uninstall ai-sloppy-copy@ai-sloppy-copy
claude plugin marketplace update ai-sloppy-copy
claude plugin install ai-sloppy-copy@ai-sloppy-copy --scope user
```

Start Claude Code, run `/reload-plugins`, review `/hooks`, and start a fresh
session. Confirm the plugin:

```powershell
claude plugin list --json
```

For either host, confirm `ai-sloppy-copy@ai-sloppy-copy` is installed and
active.

In Codex, ask:

> Use AI Sloppy Copy to revise this text: We can leverage this cutting-edge
> system to turbocharge production.

In Claude Code, use the plugin's namespaced skill command:

```text
/ai-sloppy-copy:ai-sloppy-copy

Revise this text: We can leverage this cutting-edge system to turbocharge
production.
```

The response should replace the flagged phrases with specific wording. If the
plugin is missing, repeat step 1 and restart Codex. Do not copy plugin files
into application folders manually.

## How it works

![Verified sources and approved voice move through the local checker before human approval.](plugins/ai-sloppy-copy/assets/workflow.svg)

The shared skill applies the writing contract. Both host protocols use the same
hooks and checker against the same 2.2.0 rule file. The Python checker handles
repeatable file scans. Protected text and human approval remain explicit
boundaries.

## Use the checker directly

The checker uses only the Python standard library:

```powershell
python plugins/ai-sloppy-copy/scripts/ai_sloppy_copy.py `
  --rules plugins/ai-sloppy-copy/scripts/AI-Sloppy-Copy-Rules.json `
  path/to/draft.docx
```

Supported inputs: TXT, Markdown, CSV, JSON, HTML, XML, and DOCX.

- Exit code `0`: no hard violations.
- Exit code `1`: one or more hard violations.

## Update or remove

Update:

```powershell
codex plugin marketplace upgrade ai-sloppy-copy
codex plugin remove ai-sloppy-copy
codex plugin add ai-sloppy-copy@ai-sloppy-copy
```

```powershell
claude plugin marketplace update ai-sloppy-copy
claude plugin update ai-sloppy-copy@ai-sloppy-copy
```

Remove:

```powershell
codex plugin remove ai-sloppy-copy
codex plugin marketplace remove ai-sloppy-copy
```

```powershell
claude plugin uninstall ai-sloppy-copy@ai-sloppy-copy
claude plugin marketplace remove ai-sloppy-copy
```

## Chief of Staff stack

AI Sloppy Copy is also included in the recommended
[Codex Chief of Staff](https://github.com/plotdevice01/codex-chief-of-staff)
installation. Its guide installs the complete companion stack in order.

## Privacy and security

The checker runs locally. The plugin has no connectors, accounts, telemetry, or
network calls. Its hooks receive host hook data and write only a temporary
per-session retry counter.

Do not put secrets or private client text into custom rule datasets. Report a
security issue through
[GitHub private vulnerability reporting](https://github.com/plotdevice01/ai-sloppy-copy/security/advisories/new).

See [SECURITY.md](SECURITY.md) for the support policy.

## Development

```powershell
python tests/test_runtime.py
claude plugin validate .
python scripts/build_release.py
```

Every tagged release produces a deterministic portable ZIP. The release archive
contains the same plugin, rules, documentation, and visual assets as this
repository.

See [CONTRIBUTING.md](CONTRIBUTING.md),
[CHANGELOG.md](CHANGELOG.md), and
[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

## License

[MIT](LICENSE). Third-party source notices and licenses are listed in
[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
