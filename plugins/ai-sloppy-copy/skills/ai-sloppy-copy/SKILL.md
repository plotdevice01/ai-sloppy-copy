---
name: ai-sloppy-copy
description: Check, edit, or review assistant-authored copy, replies, email, reports, captions, headings, tables, UI text, recommendations, testimonials, case studies, and long-form fiction under the AI Sloppy Copy Standard. Use when writing client-facing prose, removing model-written patterns, grounding named-person copy in verified evidence, applying a voice profile, or returning a compliance report.
---

# AI Sloppy Copy

Apply this skill to assistant-authored prose whether or not the project has its
own writing instructions.

## Required rules

- Write plain sentences from facts, actions, owners, dates, numbers, decisions,
  blockers, and next steps.
- Never use a hard-block term or expression from the bundled rule file.
- Never use em dashes or en dashes in authored prose.
- Use decorative emoji only when the user requests it.
- Use sentence case for headings unless required wording says otherwise.
- Keep measured uncertainty and source limits. Never invent facts or citations.
  Never invent opinions, experience or sensory details.
- Ground named-person endorsements and case claims in the writer's relationship
  plus a verified firsthand incident, a decision or a measured result.
- Use only owner-approved voice samples. Never manufacture errors, personal
  details, or random variation to imitate human writing.
- Never promise detector passage or report an authorship probability.
- Remove empty setup, recap paragraphs and staged contrasts. Remove unsupported
  authority claims, canned transitions and slogan fragments.
- Rewrite from the sentence's concrete meaning. A synonym swap is not a repair.
- Package rules outrank voice samples. Profiles cannot weaken hard rules.

## Evidence and voice gate

Before long-form copy in a named person's voice, or any recommendation,
testimonial, endorsement, or case study:

1. Record the writer, audience, relationship or authority, purpose, source
   facts, and approval status.
2. Require a verified firsthand incident, a decision or a measured result for
   material endorsement or case claims. If it is missing, ask for it or return
   a source-bounded draft and name the gap outside the draft.
3. Use only owner-approved voice samples. Preserve recorded diction and sentence
   habits. Never add errors, slang, memories, opinions, sensory details, or
   random variation to make text appear human.
4. Never promise detector passage or report an authorship probability. Report
   rule compliance and evidence coverage as separate checks. Report
   voice-source status and owner approval separately too.

## Workflow

1. Identify authored prose and protected text.
2. Preserve facts, stance, source limits, names, numbers, dates, and required wording.
3. Apply the evidence and voice gate when the format requires it.
4. Draft in plain language.
5. Run the bundled checker. Resolve the host's `PLUGIN_ROOT` or
   `CLAUDE_PLUGIN_ROOT` to this plugin's installed root:

```powershell
py -3 "<PLUGIN_ROOT>\scripts\ai_sloppy_copy.py" --rules "<PLUGIN_ROOT>\scripts\AI-Sloppy-Copy-Rules.json" "C:\path\to\output.docx"
```

On macOS or Linux, use `python3` and forward slashes.

6. Repair each hard failure from the sentence's concrete meaning.
7. Review warning and review rules that apply to the requested format.
8. Check again. Stop after two repair passes.
9. Return only the corrected work unless the user requests an audit.

## Protected text

Do not change exact quotes, code, commands, paths, API fields or legal text.
Keep required product or vendor wording exact. Also keep exact any text the
user orders you to preserve.
Mark exact quotes as block quotes and code as fenced or inline code when
practical. Use an owner-approved technical glossary for other required terms.

## Profiles

Voice profiles and the long-form fiction profile are opt-in. Package hard rules
always take priority. Never add facts, opinions, experience, memories, sensory
details, or story traits solely to make text appear human.

## Audit output

When asked for a compliance report, list the rule ID, passage, enforcement
level, and required edit. Do not return an authorship judgment or AI probability.
