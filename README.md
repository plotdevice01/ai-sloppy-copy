# AI Sloppy Copy

[![CI](https://github.com/plotdevice01/ai-sloppy-copy/actions/workflows/validate.yml/badge.svg)](https://github.com/plotdevice01/ai-sloppy-copy/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/plotdevice01/ai-sloppy-copy)](https://github.com/plotdevice01/ai-sloppy-copy/releases/latest)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

AI Sloppy Copy is a Codex plugin that helps produce evidence-backed prose in an
approved voice, catches common model-written patterns, and blocks hard rule
violations before the response is returned.

It does not identify whether a person or model wrote text or promise
AI-detector results. Rule compliance and authorship are separate questions.

## Install in Codex

### Before you start

You need:

- [Codex](https://developers.openai.com/codex/) with plugin support;
- [Python 3](https://www.python.org/downloads/) available as `python` on
  Windows or `python3` on macOS/Linux;
- internet access for the two install commands.

### 1. Install the marketplace and plugin

Open a terminal. On Windows, use PowerShell or the Codex terminal. Paste these
commands one at a time:

```powershell
codex plugin marketplace add plotdevice01/ai-sloppy-copy
codex plugin add ai-sloppy-copy@ai-sloppy-copy
```

If the marketplace is already installed, update it instead:

```powershell
codex plugin marketplace upgrade ai-sloppy-copy
```

### 2. Restart and trust the hooks

1. Restart the Codex desktop app, or start a new `codex` session.
2. Open `/hooks`.
3. Review and trust the `UserPromptSubmit` and `Stop` hooks from
   `ai-sloppy-copy`.
4. Start a new Codex task.

### 3. Confirm the install

Run:

```powershell
codex plugin list --json
```

Confirm `ai-sloppy-copy@ai-sloppy-copy` is installed and enabled. Then ask:

> Use AI Sloppy Copy to revise this text: We can leverage this cutting edge
> system to turbocharge production.

The response should replace the flagged phrases with concrete wording.

If the plugin does not appear, repeat step 1 exactly and restart Codex. Do not
copy plugin files into application folders manually.

## What it enforces

- Evidence gates for recommendations, testimonials, case studies, and claims.
- Owner-approved voice samples for named-person copy.
- Exact preservation of quotes, code, commands, paths, IDs, legal text, and
  required vendor wording.
- Hard rules cover banned terms and stock expressions. They also cover
  formatting habits and unsupported authorship claims.
- Review rules that need human judgment instead of a reckless search-and-replace.

The package includes 288 term rules and 21 expression rules. It also includes
34 style rules and 62 regression cases.

## Use the checker directly

The checker uses only the Python standard library:

```powershell
python plugins/ai-sloppy-copy/scripts/ai_sloppy_copy.py `
  --rules plugins/ai-sloppy-copy/scripts/AI-Sloppy-Copy-Rules.json `
  path/to/draft.docx
```

Supported inputs: TXT, Markdown, CSV, JSON, HTML, XML, and DOCX.

Exit code `0` means no hard violations. Exit code `1` means at least one hard
violation was found.

## Update or remove

```powershell
codex plugin marketplace upgrade ai-sloppy-copy
codex plugin remove ai-sloppy-copy
codex plugin add ai-sloppy-copy@ai-sloppy-copy
```

To remove it:

```powershell
codex plugin remove ai-sloppy-copy
codex plugin marketplace remove ai-sloppy-copy
```

## Chief of Staff stack

AI Sloppy Copy is one part of the recommended
[Codex Chief of Staff](https://github.com/plotdevice01/codex-chief-of-staff)
installation. The Chief of Staff guide installs the full three-plugin stack in
the correct order.

## Privacy and security

The checker runs locally. The plugin has no connectors, accounts, telemetry, or
network calls. Its hooks receive Codex hook data and write only a temporary
per-session retry counter.

Do not put secrets or private client text into custom rule datasets. Report
security issues through
[GitHub private vulnerability reporting](https://github.com/plotdevice01/ai-sloppy-copy/security/advisories/new).

## Development

```powershell
python tests/test_runtime.py
python scripts/build_release.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md), and
[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

## License

MIT. Third-party source notices and licenses are listed in
[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
