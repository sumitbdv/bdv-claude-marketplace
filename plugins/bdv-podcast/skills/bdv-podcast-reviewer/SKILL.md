---
name: bdv-podcast-reviewer
description: Audit a draft BDV podcast script against the 7-section structure, length budget, brand voice rules, and UK medical-advert compliance. Use when the user says "review the script for [topic]", "audit this script", "compliance check this", or asks for a structural pass before Dr Vali signs off.
allowed-tools: mcp__claude_ai_Google_Drive__read_file_content, Read, Bash, Write, Edit
---

# BDV Podcast Reviewer

**BDV Style Guide (Google Doc) ID:** `1mvk6zxCFWZTaX2OhYTLQOpjRL7Zn1xb50vGo07RMR4Y`

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
The canonical structure is **13 sections + tail blocks**, matching the sample reference script (Focus Deep Dive v5, Drive ID `1uPG17qcTdM7rjLX9erDP45Ng98IkQHGost5a7LKd3N0`). Fetch the sample via the Drive MCP if you need to refresh — it is the source of truth.

Required sections in order:
1. Opening Hook: The Misdiagnosis
2. The [Mechanism Metaphor]: What It Is and How It Works
3. Symptoms It Affects
4. The Rhythm Problem (or topic-equivalent reframe)
5. Testing: What Your Doctor Is Not Checking
6. What to Watch For: The [X] Trap
7. How We Do It at BDV: [3-LAYER PROTOCOL NAME]
8. The Case Studies
9. [Number] Questions to Ask Your Doctor
10. How I Personally Approach It
11. BDV Verdict
12. Closing Hook
13. Tail blocks: SCRIPTED REELS (×3) + PRODUCTION NOTES + KEY QUOTABLES

Other must-haves:
- Frontmatter with topic / lab / format / word_count_estimate / sources_used / case_studies
- Production notes block at the end (B-roll, graphics, audio cues, outfit colour)

### 2. Length pass
- **Total word count between 3,500 and 4,000 (target).** 3,200-4,200 = warn. Outside = fail. Hard ceiling 4,200.
- Section budgets (warn, don't fail, if any one section is more than 40% over):
  - S1 Opening Hook ~340 · S2 Mechanism ~450 · S3 Symptoms ~250 · S4 Rhythm ~200 · S5 Testing ~340 · S6 Trap ~250 · S7 BDV Protocol ~750 (largest) · S8 Cases ~300 · S9 10 Questions ~250 · S10 Personal ~200 · S11 Verdict ~120 · S12 Closing ~250

### 3. Section-specific structural checks
- **S1**: cold-open archetype + self-deprecating Dr Vali line + 4-6 patient voices + closing stat-stack.
- **S2**: vivid mechanism metaphor + 4-7 sub-systems with specific numbers + "what happens when it all fails" cascade.
- **S3**: 4-category symptom cluster (Physical/Cognitive/Emotional/Sleep or topic-equivalent) + age stratification (20s/30s/40s/50s) + Male pattern vs Female pattern.
- **S4**: "you don't have X problem, you have Y problem" reframe + 3 "supervillains" + 5-6 lifestyle foundations.
- **S5**: 7-9 specific tests + a single bold **DR. V'S TAKE** paragraph at the close.
- **S6**: 3-4 specific compounds/practices that backfire + **DR. V'S TAKE** verdict.
- **S7**: 3-layer protocol with clear order + 5 BDV labs in canonical order (Face/Skin/Hair/Body/Wellness) + supplement essentials + at-home biohacking + timeline + three-word recap close.
- **S8**: exactly 3 composite patients, mixed gender + ages, all labelled fictional at end, each with demographics/testing/approach/outcome/quoted line.
- **S9**: exactly 10 numbered questions, each with one-line `why`, ending with "Comment [SAFEWORD]" CTA.
- **S10**: first-person, self-deprecating vignette, 4-5 personal protocol items.
- **S11**: framing question + "The verdict?" + three-word recap.
- **S12**: two case-study follow-up vignettes + CTA stack + next-week cliffhanger + outfit-colour brief + "Look Like a Superstar. Perform Like a Legend." sign-off (repeated twice).
- **Tail**: 3 reels each with the 7 sub-fields (title text, thumbnail, visual hook, spoken hook, body, close, dopamine hits) + 7-rule Production Notes block + 10 numbered Key Quotables.

### 4. Case-study pass
- **Exactly 3 composites** (not 1, not 4)
- Naming convention `Composite [A|B|C]. [Male|Female], [age]. The [one-line label].`
- Mixed gender + age range across the three
- All labelled fictional at the end ("All composites are fictional. Built from real patterns.")
- Each block contains: demographics line + testing findings (3-5 specific numeric markers) + BDV approach (3-5 named interventions) + outcome at N weeks (with specific %) + one quoted patient line
- Use the taxonomy's named case studies (Melasma bride, Dubai couple, etc.) where the Sheet flags them

### 5. Compliance pass (UK / MHRA / ASA)
Run these regex / lexical checks and flag every hit:
- **Peptide compound names** appearing outside `{{NO_CAPTION}}` markers — they're allowed in spoken script only, never in captions. List every occurrence.
- **Unqualified medical claims**: "cures", "guaranteed", "permanent", "100%", "miracle" — fail.
- **Off-license drug names without "talk to your doctor"** — fail. Look for: tirzepatide, semaglutide, ozempic, mounjaro, retatrutide, finasteride, dutasteride, oral minoxidil, accutane / isotretinoin, HRT, TRT.
- **Specific brand drug names** in patient quotes — replace with class names.
- **Before/after numbers without a study citation** — warn.
- **"Talk to your doctor" missing entirely** — fail.

### 6. Voice pass
First fetch the **BDV Style Guide** via `mcp__claude_ai_Google_Drive__read_file_content` with the Doc ID above — it's the authoritative voice reference and the "words to avoid" / red-flag lists below are drawn from it (Dr Vali edits the Doc as the voice evolves, so prefer it if it has grown). Flag every instance of:
- Filler / hedging: "really", "very", "actually", "honestly", "obviously", "basically", "sort of", "kind of" (Style Guide §4 "Words to AVOID", §8 red flags)
- Generic wellness clichés: "journey", "nourish", "nurture", "gentle", "self-care" (non-clinical), "wellness journey"
- Victim language: "suffering", "struggling", "battling" — should be "experiencing" / "dysregulated"
- "anti-aging" / "aging gracefully" — should be "aging functionally" / "longevity"
- "we" used to mean Dr Vali personally (should be "I")
- Mangled trademarks: "BAC-12" / "bac12", "oscillations" alone (should be "Trans-Anatomical Oscillations®"), "perfect canvas" without ™ on first use
- Sentences longer than 30 words (warn — Dr Vali speaks short)
- Celebrity name-drops (fail unless flagged in production notes)

### 7. CTA pass
- **Section 9** must end with: "Comment [SAFEWORD] and we will send you the PDF tonight."
- **Section 12** must contain: Spotify follow + share + 5-star review stack, the "Comment [SAFEWORD]" repeat, the next-week cliffhanger sentence, the outfit-colour brief, and the sign-off "Look Like a Superstar. Perform Like a Legend." (repeated as two separate single-line sentences at the very end).

### 8. Lead magnet pass
Section 9 must contain:
- The "screenshot this" or "Take these to your next appointment" line
- Music drop / silence cue
- **Exactly 10 numbered questions**, each with a one-line `why` underneath
- The "Comment [SAFEWORD]" CTA at the close

### 9. Tail-block pass
- **3 scripted reels** (not 2, not 4), each with all 7 sub-fields populated (title text / thumbnail / visual hook / spoken hook / body / close / dopamine hits)
- Each reel labelled `REEL [N] | [LABEL] | THE 360 | EP[X] | 60 sec`
- Each reel has exactly 2 dopamine hits identified
- **Production Notes** contain all 7 Content Masterclass rules verbatim
- **Key Quotables** contains exactly 10 numbered quotables, all pulled from the script's actual lines

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
