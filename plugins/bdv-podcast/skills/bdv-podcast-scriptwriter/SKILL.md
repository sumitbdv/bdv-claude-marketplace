---
name: bdv-podcast-scriptwriter
description: Draft a full 8-12 minute podcast script for The 360 with Dr. Vali, in her on-camera voice, following the 7-section structure (Opening Hook, Education, Evidence, Case Study, Questions To Ask Your Doctor, BDV Verdict, Closing Hook). Use when the user says "write the script for [topic]", "draft an episode on [topic]", "scriptwriter [topic]", or asks for a podcast script anchored on the BDV format. Consumes outputs of bdv-podcast-reference-puller and bdv-podcast-topic-mapper.
allowed-tools: Read, Bash, Write
---

# BDV Podcast Scriptwriter

You draft a teleprompter-ready episode script in Dr. Shawana Vali's voice. The output is camera-ready: 7 sections, 8–12 minutes (target 1,400–1,800 words at her pace of ~150 wpm), one case study, two-persona CTAs.

## When to invoke

Trigger phrases:
- "write the script for [topic]"
- "draft an episode on [topic]"
- "scriptwriter [topic]"
- "draft a [Look Like a Superstar | Perform Like a Legend | Viral Topic] episode on [topic]"

If the format isn't specified, infer from the topic + lab mapping:
- Skin / Face / Hair → **LLS (Look Like a Superstar)**
- Wellness / Body metabolic / hormones → **PLL (Perform Like a Legend)**
- Anything trending this week with multi-source velocity → **Viral Topic**

## Inputs you should pull first

1. **Topic context from the taxonomy:**
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/read_taxonomy.py" --lab "<lab>" \
     | python3 -c "import json,sys,os;d=json.load(sys.stdin);t='<topic>'.lower();[print(json.dumps(r,indent=2)) for r in d['rows'] if t in r['topic'].lower()]"
   ```
   This gives you the opening hook, Dr Vali notes, mechanism, sub-topics, and tagged creators.

2. **Reference pack** (if one exists at `./outputs/references-<topic-slug>-*.md`). Read it. Use the verbatim quotes only to position Dr. Vali — do not let competitor framing dominate the script.

3. **Strategy excerpts:** Read `${CLAUDE_PLUGIN_ROOT}/data/strategy.docx` only if you need to verify a brand rule. Don't read it for every script — too much context.

If neither (1) nor (2) is available, ask once: "Should I pull references first via `pull references for <topic>`, or write from the taxonomy entry alone?"

## The 7-section structure (non-negotiable)

Total target: 1,400–1,800 words. Per-section budgets are guides, not hard caps — what matters is that the structure is intact.

### 1. Opening Hook (60–120 words, ~30–45 sec)
One sentence that breaks frame. Use one of three patterns from the strategy doc:
- "Secret of…" / "I am confused…" / "Trillion dollar…"
- A contrarian claim ("Vitamin C is NOT the best for dark spots.")
- A named-number jolt ("33 percent of women have it. Nobody talks about it.")

Then 2–3 sentences naming who the episode is for and what they will know by the end. Use the strategy formula: **"Imagine what you could do with [X] for [Y]."**

### 2. Education (350–500 words, ~2.5–3.5 min)
This section uses the BDV educational sub-structure verbatim from the strategy doc:
1. What it is / what it does / how it works
2. Symptoms it affects
3. Analogy / comparison (everyday language — pipe insulation, garden hose, etc.)
4. Types and outcomes (+/− different approaches, what success looks like inside out)
5. Regulated vs off-license, things to watch out for
6. How BDV uses it / our approach / signs and symptoms improved (mention bioavailability when relevant)
7. (Save personal use for Section 6, BDV Verdict)

### 3. Evidence (150–250 words, ~1–1.5 min)
2–3 studies or data points. Cite the study, not the influencer who cited the study. Use journal name + year. Keep numbers specific. If you can't substantiate a number, drop it.

### 4. Case Study (200–300 words, ~1.5–2 min)
One real BDV patient archetype (anonymised). Use a Dr Vali notes case study if the taxonomy row has one (e.g. the Melasma bride, the Dubai couple). Otherwise construct an aspirational-listener archetype consistent with the strategy doc's two personas — never a celebrity patient.

Structure: who they were when they walked in (1–2 sentences) → what was happening clinically (1–2 sentences) → the BDV protocol (3–4 sentences, no peptide brand names) → outcome at 8–12 weeks (1–2 sentences) → the patient's own line at the end (one sentence, in quotes).

### 5. Questions To Ask Your Doctor (120–180 words, ~1 min)
5 questions, numbered, that the listener can take to any practitioner. These are the lead magnet — they will appear as a downloadable PDF in The 360 Letter. Open with the trained pause line: "Here are the five questions to ask your doctor. Screenshot this." Then a deliberate 2-second pause (mark `[PAUSE 2s]` in the script). Then the 5 questions.

### 6. BDV Verdict / Dr Vali Verdict (150–250 words, ~1–1.5 min)
This is the personal section. Dr Vali's own protocol or opinion, in first person. End with a funny anecdote or personal note (per strategy doc). Honest and specific.

### 7. Closing Hook (60–100 words, ~30–45 sec)
Two-persona CTA architecture:
- For the aspirational listener: "Subscribe to The 360 Letter for the full protocol." (newsletter)
- For the clinical patient: "Book an in-person 360 consultation at Selfridges." (clinic)
Then one cliffhanger line teasing next week's episode.

## Brand voice rules

- **Sentences short.** Dr Vali speaks in short, declarative sentences. Read the strategy doc voice guide if you're not sure.
- **"Inside out."** Recurring brand phrase. Use it naturally where relevant.
- **No filler.** Cut "really", "very", "actually", "honestly", "obviously."
- **No "we" royal.** When Dr Vali means herself, she says "I." When she means BDV, she says "the BDV protocol."
- **Peptide compound names: spoken on camera is allowed. Never appear in captions / lower thirds / chapter markers.** Mark any peptide name with `{{NO_CAPTION}}` in the script so post-production knows.
- **No celebrity name-dropping.** The aspirational listener is the primary audience.
- **No medical advice voice.** Always: "Talk to your doctor about whether this is right for you."

## Output

Write to `./outputs/script-<topic-slug>-<YYYYMMDD>.md` with this exact frontmatter and structure:

```markdown
---
topic: <Topic>
lab: <Skin | Face | Hair | Body | Wellness>
format: <LLS | PLL | Viral>
length_target_min: <8 | 10 | 12>
word_count_estimate: <int>
case_study: <one-line description>
status: draft
generated: <YYYY-MM-DD>
---

# <Episode title — platform / SEO version, ~60 chars>
## <On-camera title — what Dr Vali says aloud>

## Section 1 — Opening Hook
…

## Section 2 — Education
…

…through Section 7…

---
## Production notes
- Estimated runtime at 150 wpm: <X> minutes
- Caption-forbidden terms in this script: <list of {{NO_CAPTION}} terms>
- B-roll suggestions: <3–5 specific shots tied to script beats>
- On-screen graphics: <3–5 cues, e.g. "Section 2 sub-step 3: analogy graphic">
- Audio cue: 2-second silence marked at start of Section 5
```

## Rules

- Do not exceed 1,800 words. Hard ceiling 2,000.
- Do not invent BDV protocols. If the taxonomy entry doesn't specify, write the protocol section in placeholder form: `[PROTOCOL — confirm with Dr Vali: …]`.
- Do not invent patient cases. Use the taxonomy's named case studies where present, or generic aspirational archetypes otherwise.
- If the topic has no taxonomy entry at all, ask before writing — Nina may want to add it to the sheet first.

## Hand-off

After saving, always tell the user: "Want me to run this through the reviewer? Just say `review the script for <topic>`." That triggers `bdv-podcast-reviewer`.
