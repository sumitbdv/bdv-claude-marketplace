---
name: bdv-podcast-reviewer
description: Audit a draft BDV podcast script against the 7-section structure, length budget, brand voice rules, and UK medical-advert compliance. Use when the user says "review the script for [topic]", "audit this script", "compliance check this", or asks for a structural pass before Dr Vali signs off.
allowed-tools: Read, Bash, Write, Edit
---

# BDV Podcast Reviewer

You audit a draft script and return a redline + an actionable checklist. Output is two artifacts: (1) the script with inline `[REVIEW: …]` annotations, and (2) a one-page audit summary Dr Vali can read in 60 seconds.

## When to invoke

Trigger phrases:
- "review the script for [topic]"
- "audit this script"
- "compliance check this"
- "review the draft on [topic]"

## Locate the draft

If the user supplies a path, use it. Otherwise find the most recent matching file in `./outputs/script-*.md` (newest first). If multiple match, ask which one.

## The audit, in order

Run all checks. Don't stop at the first failure.

### 1. Structural pass (must-haves)
- All 7 sections present (Opening Hook, Education, Evidence, Case Study, Questions To Ask Your Doctor, BDV Verdict, Closing Hook), in order
- Frontmatter present with topic / lab / format / word_count_estimate
- Production notes block present at the end

### 2. Length pass
- Word count between 1,400 and 1,800 (target). 1,200–2,000 = warn. Outside = fail.
- Section budgets (warn, don't fail, if any one section is more than 50% over):
  - Opening Hook 60–120 · Education 350–500 · Evidence 150–250 · Case Study 200–300 · QTAYD 120–180 · Verdict 150–250 · Closing 60–100

### 3. Education sub-structure pass
Confirm Section 2 covers the 7 BDV educational steps (what it is / symptoms / analogy / types / regulation / BDV approach / personal use deferred to S6). Flag any missing step.

### 4. Case study pass
- One case study, not multiple
- Anonymised (no real names)
- Includes outcome at 8–12 weeks
- Includes one quoted line from the patient
- Aspirational-listener archetype, not a celebrity patient

### 5. Compliance pass (UK / MHRA / ASA)
Run these regex / lexical checks and flag every hit:
- **Peptide compound names** appearing outside `{{NO_CAPTION}}` markers — they're allowed in spoken script only, never in captions. List every occurrence.
- **Unqualified medical claims**: "cures", "guaranteed", "permanent", "100%", "miracle" — fail.
- **Off-license drug names without "talk to your doctor"** — fail. Look for: tirzepatide, semaglutide, ozempic, mounjaro, retatrutide, finasteride, dutasteride, oral minoxidil, accutane / isotretinoin, HRT, TRT.
- **Specific brand drug names** in patient quotes — replace with class names.
- **Before/after numbers without a study citation** — warn.
- **"Talk to your doctor" missing entirely** — fail.

### 6. Voice pass
Flag every instance of:
- "really", "very", "actually", "honestly", "obviously", "basically" (filler)
- "we" used to mean Dr Vali personally (should be "I")
- Sentences longer than 30 words (warn — Dr Vali speaks short)
- Celebrity name-drops (fail unless flagged in production notes)

### 7. CTA pass
Closing Hook must contain both two-persona CTAs:
- Aspirational listener → newsletter ("The 360 Letter")
- Clinical patient → in-person consult at Selfridges
Plus one cliffhanger for next week.

### 8. Lead magnet pass
Section 5 must contain:
- The "screenshot this" line
- `[PAUSE 2s]` marker
- Exactly 5 numbered questions

## Output

**Artifact 1** — annotated script:
- Copy the draft to `./outputs/script-<slug>-<date>.reviewed.md`
- Insert `[REVIEW: <issue>]` inline at every flagged spot. Don't rewrite — annotate.

**Artifact 2** — audit summary:
Save to `./outputs/audit-<slug>-<date>.md`:

```markdown
# Script audit — <Topic>
_Reviewed <date> from <input path>._

## Verdict
<one of: READY FOR DR VALI · NEEDS REVISION · DO NOT FILM>

## Pass / fail summary
- Structure: <pass | fail — reason>
- Length: <pass | warn | fail — word count>
- Education sub-structure: <pass | fail>
- Case study: <pass | fail>
- Compliance: <pass | fail — list>
- Voice: <N filler hits, M long sentences>
- CTA: <pass | fail>
- Lead magnet: <pass | fail>

## Top 5 fixes, in priority order
1. <issue> — <fix>
2. …
3. …
4. …
5. …

## All flagged items
<comprehensive list with line refs to the annotated file>
```

## Rules

- **Never edit the script in place.** Always work on a `.reviewed.md` copy.
- **Be specific.** "Section 5 missing PAUSE 2s marker on line 87" beats "fix the lead magnet."
- **Compliance is binary.** A compliance fail is `DO NOT FILM` no matter how good the rest is.
- **Voice flags are warnings, not failures.** Dr Vali decides what to keep.
- **Keep the audit summary under 400 words.**

## Hand-off

End with: "Verdict is <verdict>. Want me to apply the top 5 fixes? Say `apply audit fixes` and I'll edit the script in place." If the user says yes, only then make edits.
