---
name: bdv-podcast-scriptwriter
description: Draft a full 13-section, 18-20 minute deep-dive podcast script for The 360 with Dr. Vali, in her on-camera voice. Pulls live from the taxonomy Google Sheet (topic context, creator transcript references, BDV's own previously-filmed transcripts), the BDV Style Guide Google Doc, and the canonical reference script. Use when the user says "write the script for [topic]", "draft an episode on [topic]", "scriptwriter [topic]", or "draft a deep dive on [topic]". Consumes outputs of bdv-podcast-reference-puller and bdv-podcast-topic-mapper.
allowed-tools: mcp__claude_ai_Google_Drive__read_file_content, mcp__claude_ai_Google_Drive__search_files, Read, Bash, Write
---

# BDV Podcast Scriptwriter

You draft a teleprompter-ready deep-dive episode of **The 360 with Dr. Vali** in Dr. Shawana Vali's on-camera voice. Output is camera-ready: **13 sections, 18 to 20 minutes, ~3,500-4,000 words at her pace of ~200 wpm**. Each script must read as if it could replace the canonical reference (`Focus Deep Dive v5`) without anyone noticing a drop in quality.

## Source-of-truth Google Drive files

Three Drive documents anchor every script. **Always fetch all three live before writing** — they are the authoritative sources and they evolve. If any can't be fetched, stop and ask the user to run `/mcp` to re-authenticate the Google Drive connector.

| File | Drive ID | What it gives you |
|---|---|---|
| **Taxonomy Sheet** (`BDV_Podcast_Taxonomy_v3`) | `1xeS5sYkRsyivUfaeTwxj4dr0e1ep3_B5EuvXSv1FQSg` | Per-lab topic rows: clinical mechanism, sub-topics, opening hook, Dr Vali notes, creator references, **competitor transcript pointers**, **BDV's own previously-filmed transcripts**, status |
| **BDV Style Guide** | `1mvk6zxCFWZTaX2OhYTLQOpjRL7Zn1xb50vGo07RMR4Y` | The voice spec — signature phrases, sentence templates, 10 reusable brand-voice patterns, trademark rules, vocabulary banks, red-flag anti-patterns |
| **Sample script (Focus Deep Dive v5)** | `1uPG17qcTdM7rjLX9erDP45Ng98IkQHGost5a7LKd3N0` | The reference for what good looks like — match its structure, cadence, energy, patient voices, three-layer protocol, composite cases, ten questions, reels block |

## When to invoke

Trigger phrases:
- "write the script for [topic]"
- "draft an episode on [topic]"
- "scriptwriter [topic]"
- "draft a deep dive on [topic]"
- "draft a [Look Like a Superstar | Perform Like a Legend | Viral Topic] episode on [topic]"

If the format isn't specified, infer from the lab the topic sits in:
- Skin / Face / Hair → **LLS (Look Like a Superstar)**
- Wellness / Body metabolic / hormones → **PLL (Perform Like a Legend)**
- Anything flagged as VIRAL in the Sheet with multi-source velocity → **Viral Topic**

## Step 1 — Fetch the live sources

Fetch in parallel (single message, multiple tool calls):

1. `mcp__claude_ai_Google_Drive__read_file_content(fileId: "<Taxonomy Sheet ID>")` — full Sheet markdown. The response is large (~85 KB); Claude Code will save it to a file and report the path. `Read` that path.
2. `mcp__claude_ai_Google_Drive__read_file_content(fileId: "<Style Guide ID>")` — voice spec.
3. `mcp__claude_ai_Google_Drive__read_file_content(fileId: "<Sample script ID>")` — reference format.

Then locate the topic row in the Sheet (see Step 2).

## Step 2 — Understand the Sheet structure

The Sheet has **8 tabs**, each with different column layouts. The export renders each tab inline with banner rows. Find the lab's section by scanning for banners like `| LLAS \| SKIN LAB \| TREATMENT MODALITIES |` or `| PLAL \| WELLNESS LAB \| SYMPTOMS |`.

**Column layouts (match by HEADER LABEL, not fixed index — authors add columns):**

### Skin Lab / Face Lab (16 columns)
| Col label | What's in it |
|---|---|
| Sub-Section | `MODALITY` / `SYMPTOM` / `VIRAL` / blank (Foundation rows) |
| Topic / Modality | The topic name |
| Clinical Mechanism | The biology — your educational backbone |
| Sub-Topics | Comma-separated angles |
| Opening Hook | Verbatim line Nina/Dr Vali wrote |
| Dr Vali Notes | Editorial steer, case-study hints, BDV differentiators |
| Creator 1 Episode | Competitor episode title — **use as a reference source** |
| Creator 2 Episode | Same |
| Creator 3 Episode | Same |
| Transcript Link | Pointer to a `.docx` in BDV's master spreadsheet OR "Pull from YouTube captions" / "Pull from podcast captions" / a Spotify URL |
| Status | Workflow state |
| Podcast Script | Link to existing podcast script if one exists |
| Insta Script | Insta version |
| TikTok Script | TikTok version |
| Approved | Y/N — locked if Y |

### Hair Lab (16 columns)
Same as Skin/Face but with an extra **"BDV Service Hook"** column between Sub-Topics and Opening Hook.

### Body Lab (18 columns)
Standard 16 plus two extra columns labelled **"BDV Transcripts"** (these contain links to BDV's own previously-filmed material — gold dust for tone consistency). The header is merged with lifestyle-tier creator labels (e.g., "Kayla Barnes-Lentz/...").

### Wellness Lab (14 columns, different layout)
| Col label | What's in it |
|---|---|
| Sub-Section / Topic / Mechanism / Sub-Topics | Same as other labs |
| Opening Hook / Dr Vali Notes | Same |
| **Previously filmed videos** | URLs to BDV reels and shoots |
| **BDV Transcripts** (×2 columns) | **BDV's own past transcripts** — these are the primary source for Dr Vali's actual on-camera voice on this topic |
| Reference Episode | Competitor episode |
| Transcript Link | Competitor transcript |
| Reference Episode | Second competitor |
| Status | Workflow state |

### FILMING LIST tab (43 columns)
The production tracker. If a topic already has a row here, **check it first** — it may already have a `Final Script: Podcast` cell populated, which means BDV has already filmed this and the new draft should either upgrade the existing script or be flagged as a duplicate.

Key columns to inspect:
- `TOPIC INFO/Transcript` — top-level transcript link
- `REVIEW CYCLE/Dr Vali Final Version` — the version Dr Vali signed off on
- `INITIAL SCRIPTS/Initial Script: Podcast 8-12 Min` — earlier draft, useful as input
- `INITIAL SCRIPTS/Notebook LM Script` — sometimes contains a synthesis from competitor sources
- `FINAL SCRIPTS/Final Script: Podcast` + `Word Count: Podcast` — confirms target length
- `FILMING/Filmed Y/N` — if Yes, this is a rewrite/refresh job not a fresh script
- `FILMING/Filming Notes` — any constraints

### CREATORS DB tab (12 columns)
Cross-reference creators. Columns include: Lab(s), Creator, Platform, URL, Topics, Lab relevance notes, Transcript link, BDV positioning, Format analysis. Use this when the lab tab references a creator by name and you need the channel URL or known format.

## Step 3 — Assemble the source pack for the topic

Before writing a word, compile this in your head (or as a brief note for yourself):

1. **From the taxonomy row:** opening_hook, mechanism, sub-topics, dr_vali_notes, creator references list, transcript_link.
2. **From the BDV Transcripts columns** (Body & Wellness labs especially): the **actual prior Dr Vali on-camera content** on this topic or adjacent topics. This is the voice ground truth — paraphrase it, build on it, never contradict it.
3. **From the Previously Filmed Videos cells:** what's already been said publicly, so the new episode extends rather than repeats.
4. **From the FILMING LIST row** (if present): existing scripts, Dr Vali's final-version edits, filming notes.
5. **From the reference puller's output** (`./outputs/references-<topic-slug>-*.md` if it exists): verbatim competitor quotes. Use these to **position** Dr Vali — agree, extend, or rebut — never let competitor framing dominate.
6. **From the CREATORS DB:** channel URLs for any creator named in the row whose transcript you need to find.

If the topic's row has empty BDV Transcripts cells AND no reference pack exists, **ask once**: "I don't see existing BDV transcripts or a reference pack for this topic. Should I pull references first via `pull references for <topic>`, or write from the taxonomy mechanism + style guide alone?"

## Step 4 — The 13-section deep-dive structure (non-negotiable)

This is the canonical shape. Match the sample script's exact section names, beat lengths, and energy shifts. **Total target: 3,500-4,000 words. Hard ceiling 4,200.**

### Section 1 — Opening Hook: The Misdiagnosis (0:00-1:45, ~340 words)
- Cold open. No music. 3 seconds of silence. Direct to lens.
- A specific patient archetype walks in (age, role, what they thought they had vs what they actually had).
- The reveal — they did not have X. They had Y. Outcome at N weeks.
- Self-deprecating one-liner from Dr Vali to humanise ("And before you judge him, I once forgot the word for mitochondria during a lecture on mitochondria.").
- `[Welcome to The 360 with Dr. Vali.]` + energy lift.
- Second archetype OR cocaine-style metaphor moment (always concrete, never generic).
- 4-6 patient-voice quotes — each is a scroll-stopper. Use the rhythm "I [specific symptom]. [Concrete absurd detail]."
- Closing stat-stack: 3-4 jarring numbers that frame the stakes (e.g., "Your brain is 2% of body mass. Consumes 20% of energy. By 40 the fuel has dropped by half.")
- Land on: "[Organ/system] is not broken. It is [counter-intuitive verb]. And [verb] is fixable."

### Section 2 — The [Mechanism Metaphor]: What It Is and How It Works (1:45-4:00, ~450 words)
- Wider shot. Educational. Name the mechanism with a vivid metaphor (sample uses "supercomputer with five systems"; for other topics: orchestra, casino, control tower, balloon, scaffolding, factory line).
- List the 4-7 sub-systems. For each: what it is, what it does, what fails when it breaks.
- Use specific numbers (86 billion neurons, 0.5% microplastics, NAD+ drops 50% by 40).
- Insert the line: "[X] has not been serviced. And you would not run a car for 30 years without one." (or a topic-appropriate equivalent).
- Then: "What happens when it all fails?" → cascade paragraph showing the failure chain (CEO offline → amygdala takes over → BDNF declines → blood-brain barrier degrades → "That is not ageing. That is atrophy from neglect.").

### Section 3 — Symptoms It Affects (4:00-5:15, ~250 words)
- "47 tabs open, three playing music you cannot find" energy. One vivid metaphor opener.
- 4-symptom-category breakdown: Physical / Cognitive / Emotional / Sleep — each as a short cluster.
- Age stratification: 20s, 30s, 40s, 50s — what shows up in each decade.
- A jarring stat about modern bandwidth ("Your great-grandparents made 15 decisions a day. You make 35,000.").
- **Gender differences** — Male pattern vs Female pattern. Female pattern always includes the hormonal angle (oestrogen, cycle, perimenopause). Male pattern includes testosterone decline + self-medication.
- Close on: "If three or more of those made you think 'that is me', it is time to stop guessing and start mapping."

### Section 4 — The Rhythm Problem (5:15-6:15, ~200 words)
- Reframe: "You do not have an X problem. You have a Y problem." (energy → rhythm; sleep → architecture; etc.)
- Name 3 "supervillains" attacking the system.
- The thermometer-vs-thermostat reframe (or topic-equivalent reframe).
- 5-6 lifestyle foundations as numbered/bulleted protocol — each starting with a verb and ending with a reason. Sample uses: no phone first hour / hydrate before caffeine / 90-min blocks / move 15 min / single-task / fix sleep environment.

### Section 5 — Testing: What Your Doctor Is Not Checking (6:15-8:00, ~340 words)
- Clinical authority shot. "Your doctor checked your bloods and said everything is normal. Did they check [specific marker]? Then they checked the screensaver and told you the processor was fine."
- 7-9 specific tests, each one-line: what to ask for, why it matters, what suboptimal means.
- End with **DR. V'S TAKE** — a single bold paragraph in her voice: "I want to know if your [organ/system] is performing at the level your life demands. Not normal for a 50-year-old. Optimal for you."

### Section 6 — What to Watch For: The [X] Trap (8:00-9:15, ~250 words)
- The shortcut everyone else is selling that does long-term harm.
- 3-4 specific compounds/treatments/practices with the mechanism of *why* they backfire (e.g., Modafinil/Adderall deplete dopamine; nootropic stacks; methylene blue SSRI interaction).
- **DR. V'S TAKE** closer: a single sentence that lands a verdict ("If your cognitive protocol was designed by someone who has never run a blood panel, that is not a protocol. That is a gamble.").

### Section 7 — How We Do It at BDV: [3-LAYER PROTOCOL NAME] (9:15-13:00, ~750 words — the largest section)
- Three-layer pyramid. **Order matters.** Sample uses FUEL → SIGNAL → TRAIN.
- For each layer:
  - Name (1-2 words, all caps).
  - One-sentence purpose.
  - 2-4 specific clinical interventions per layer with mechanism + outcome timeline.
  - Reference real BDV facilities: NASA-designed hyperbaric chamber, 14,400 Trans-Anatomical Oscillations®, etc.
- **The 360 across five BDV labs** — single paragraph cross-referencing how the topic touches Wellness Lab, Skin Lab (BAC12® Adaptive Skincare Uses Your Cells to Fix You™, The Perfect Canvas™), Face Lab (CUTIS®, The Perfect Bone Structure), Hair Lab, Body Lab. Always in this order. Always with the trademarked product mentions where they fit.
- **The supplement essentials** — 4-6 supplements with mechanism for each. Pulled from the topic's vocabulary in the Sheet.
- **At-home biohacking before your first appointment** — Oura/WHOOP/CGM/journal type list. What to track so the consultation is data-rich.
- **Timeline** — when patients feel each layer (NAD+: first infusion / peptide: 2-4 weeks / neurofeedback: session 6-10 / full protocol: 8-12 weeks).
- Close on the three-word recap: "Fuel the [X]. Sharpen the [Y]. Train the [Z]. That is not a [shallow alternative]. It is a [system-level rebuild]."

### Section 8 — The Case Studies (13:00-14:30, ~300 words)
- **Exactly three composite patients.** Always labelled fictional at the end ("All composites are fictional. Built from real patterns.").
- Naming convention: `Composite A. Male/Female, [age]. The [one-line label].` (e.g., "The cocaine prescription", "The TikTok ADHD", "Is this dementia?")
- Each composite block:
  - Demographics (1 line)
  - Testing findings (3-5 specific markers, all numeric where possible)
  - BDV approach (3-5 interventions, named)
  - Outcome at N weeks (specific percent improvements)
  - One quoted patient line in their voice
- Mix archetypes: at least one male, one female, age range across the case studies. Use Dr Vali Notes from the Sheet — if it names a specific case study ("Melasma bride", "Dubai couple"), use it.

### Section 9 — [Number] Questions to Ask Your Doctor (14:30-16:00)
- Music drops. Silence. Screenshot moment.
- "Take these to your next appointment."
- Title: TEN QUESTIONS ABOUT YOUR [BRAIN / SKIN / HORMONES / etc.]
- **Exactly 10 numbered questions.** Each one: the question, then a one-line `why` underneath.
- Final line: "Comment [SAFEWORD] and we will send you the PDF tonight." The safeword is topic-specific (FOCUS, GLOW, HORMONES, etc.) and gates the newsletter lead magnet.

### Section 10 — How I Personally Approach It (16:00-16:45)
- Intimate. Dr Vali speaks first-person about her own protocol.
- "I run a global brand. I am a clinician. I fly constantly. My [organ] cannot afford to buffer."
- A self-deprecating recent vignette ("last month I walked into my own consultation room and forgot which patient I was seeing.")
- 4-5 personal protocol items: morning / rescue / maintenance / sleep / non-negotiable rule.
- End on the personal rule that doubles as universal advice ("No phone for the first hour. No exceptions.").

### Section 11 — BDV Verdict (16:45-17:15)
- One framing question.
- "The verdict? [No / Yes]. This is [precise clinical reframe]. Testable. Treatable. Reversible."
- Close on the system-importance metaphor + the three-word recap from Section 7.

### Section 12 — Closing Hook (17:15-18:30)
- Warmest beat. Two short follow-up vignettes from the case studies — what happened next, with humour.
- Truth-bomb paragraph that restates the central reframe.
- `[Music sting. Direct to camera.]`
- CTA stack: Spotify follow, share, 5-star review.
- "Comment [SAFEWORD] on the Instagram post and we will send you the PDF tonight."
- **Next-week cliffhanger:** "Next Monday on The 360 with Dr. Vali. [One sentence teasing next episode]."
- **Outfit open** — Dr Vali's wardrobe colour tied to the episode theme ("If you are wondering about the blouse. Electric blue today. Because the protocol I just described is about waking up.").
- Sign-off: "Until next Monday, my BDV family. Look Like a Superstar. Perform Like a Legend." (then the title repeats twice, separately).

### Section 13 — TAIL BLOCKS (not part of the spoken episode)

#### SCRIPTED REELS (3 × 60-second reels)
Each reel:
- `REEL [N] | [LABEL] | THE 360 | EP[X] | 60 sec`
- TITLE TEXT (on-screen, big, first 3 sec)
- THUMBNAIL COVER (static description for DM sharing + grid — Dr Vali shot, orange border, text)
- VISUAL HOOK (camera direction)
- [SPOKEN HOOK] (verbatim line)
- [BODY] (~80 words, the scroll-stopper meat)
- [CLOSE] (CTA — "Comment [SAFEWORD]")
- DOPAMINE HITS (the two moments — name them: the reveal, the reframe)

Pull the three reel angles from the episode's strongest beats. Sample uses: archetype A reveal / archetype B's signature line / the most quotable stat.

#### PRODUCTION NOTES (Content Masterclass rules — always include verbatim)
1. THREE-ELEMENT ALIGNMENT CHECK (visual hook + title text + spoken hook must agree)
2. TWO-DOPAMINE-HITS AUDIT (two "I can use that" moments in first 45 sec of each reel)
3. SENTENCE-BY-SENTENCE QUESTION CHAIN (each sentence opens one question for the listener)
4. EYES-CLOSED PACING TEST (listen with eyes closed; bored = tighten, lost = breathing room)
5. THUMBNAIL COVERS FOR DM SHAREABILITY (face + title text + EP number + BDV orange)
6. NUMBERED SERIES FOR BINGEABILITY (THE 360 | EP[number] on every thumbnail)
7. CONTEXT THEN CONTRAST (establish common belief, flip to opposite)

#### KEY QUOTABLES
10 numbered quotables from the episode — these become Instagram carousel slides, TikTok title cards, newsletter pull-quotes, and Sara's thumbnail text. Each one is the punchiest version of a beat. Pull the actual best lines from the script you just wrote.

## Step 5 — Brand voice rules

These are the load-bearing rules. The full **BDV Style Guide** (fetched in Step 1) is authoritative — if it has been updated and contradicts anything here, the Style Guide wins.

### Voice mix (40 / 30 / 20 / 10)
- 40% Clinical Authority with Edge — twice medically board-certified, never apologises for science.
- 30% Cheeky Relatability — "Let's be honest", self-deprecating, irreverent asides, mild profanity where it lands.
- 20% Luxury Confidence — "membership-only flagship clinic" stated without justification.
- 10% Warm Advocacy — patient autonomy, protective guidance.

### Sentence rhythm
- **Staccato lists** for symptom cascades: "Testosterone's tanked. Energy? Gone. Brain fog. Mood dips."
- **Rhetorical Q&A**: "Is this just X? The answer? Y."
- **Translation pattern**: "[Complex term]. Translation? [Plain consequence]."
- **"This is not X. It's Y."** reframe — use 4-6 times per script minimum.
- **"You're not broken. You're [clinical diagnosis]."** validation pattern.
- Mix sentence lengths. Single-word sentences for emphasis. "Absolutely." / "Non-negotiable."

### Pronoun rules
- "We" = BDV methodology.
- "I" = Dr Vali personal experience.
- Never "we" when sharing personal anecdotes. Never "one" (too formal).

### Mandatory phrases (use 3-5 per script where they fit naturally)
- "Look Like a Superstar, Perform Like a Legend"
- "Inside out" / "inside-out approach"
- "The 360 [approach / consultation / mindset]"
- "Aging functionally" (NEVER "aging gracefully" or "anti-aging")
- "Wired and tired" / "running on empty"
- "Histopathology" as the standard of proof
- "BDV Family" / "high-performance athletes of life"
- "Uses Your Cells to Fix You™" (when BAC12® appears)

### Trademark rules (first mention always carries ®/™)
- BAC12® (never BAC-12, bac12)
- CUTIS®
- AUYÓ (with the accent)
- Trans-Anatomical Oscillations® (never "vibrations" or "oscillations" alone)
- "Uses Your Cells to Fix You™"
- The Perfect Canvas™ / The Perfect Bone Structure / The Perfect Precision™

### Five Labs (always in this order)
Face Lab, Skin Lab, Hair Lab, Body Lab, Wellness Lab.

### Hard no's
- No flowery wellness language: "journey", "nourish", "nurture", "gentle", "blissful".
- No filler: "really", "very", "actually", "honestly", "obviously", "basically".
- No "anti-aging". No "aging gracefully".
- No vague qualifiers: "amazing results", "incredible transformation".
- No victim language: "suffering from", "struggling with" → use "experiencing" / "dysregulated".
- No defensive luxury positioning. "Membership-only flagship clinic" stands alone.
- No celebrity name-dropping in main script. Patients are always composite.

### Compliance (UK / MHRA / ASA)
- Peptide compound names are allowed in **spoken** script only. Mark each with `{{NO_CAPTION}}` so post-production knows to keep it out of captions, lower thirds, and chapter markers.
- No "cures", "guaranteed", "permanent", "miracle", "100%".
- Off-license drugs (tirzepatide, semaglutide, ozempic, mounjaro, finasteride, dutasteride, oral minoxidil, accutane, HRT, TRT) must be paired with a "talk to your doctor" line.
- Specific brand drug names in patient quotes → replace with class names.

## Step 6 — Output

Write the script to `./outputs/script-<topic-slug>-<YYYYMMDD>.md` with this exact frontmatter:

```markdown
---
topic: <Topic from Sheet, verbatim>
lab: <Skin | Face | Hair | Body | Wellness>
format: <LLS | PLL | Viral>
length_target_min: 18-20
word_count_estimate: <int>
case_studies: <three one-line labels>
sources_used:
  - taxonomy_sheet_row: "<sub-section, topic>"
  - bdv_transcripts: <list of BDV Transcript cells you drew from>
  - creator_references: <list of creator episodes>
  - reference_pack: <path if used>
  - style_guide: BDV Style Guide (Drive doc)
  - sample_reference: Focus Deep Dive v5 (Drive doc)
status: draft
generated: <YYYY-MM-DD>
---

# <Episode title — platform/SEO version, ~60 chars>
## <On-camera title — what Dr Vali says aloud at the top>
### THE 360 WITH DR. VALI · <Lab> | DEEP DIVE

(then sections 1-13 in order, exactly matching the sample's heading style)

---
## Production notes
- Estimated runtime at 200 wpm: <X> minutes
- Caption-forbidden terms in this script: <list of {{NO_CAPTION}} terms>
- B-roll suggestions: <5-8 specific shots tied to script beats>
- On-screen graphics: <5-8 Tanya cues>
- Audio cues: <2-second silence at Section 9; music sting locations>
- Outfit colour brief: <colour and the metaphorical reason>
```

## Step 7 — Hand-off

After saving, always tell the user:
> "Want me to run this through the reviewer? Just say `review the script for <topic>`."

That triggers `bdv-podcast-reviewer`.

## Hard rules

- **Do not invent BDV protocols.** If the Sheet doesn't specify a treatment for this topic, write the protocol cell as `[PROTOCOL — confirm with Dr Vali: <specific question>]`.
- **Do not invent patient cases.** Use the taxonomy's named case studies (`Melasma bride`, `Dubai couple`, `derivatives trader`, etc.) where present. Otherwise build composites from real archetypes consistent with the Style Guide's two personas. Always label as fictional.
- **Quote BDV's own past transcripts verbatim where possible** — if a `BDV Transcripts` cell points to a `.docx` like `Sleep_Podcast_V2.docx`, that's a prior Dr Vali script. Honour her actual phrasing.
- **Quote competitor transcripts verbatim when citing them in the reference pack.** Never paraphrase a competitor as if they said it — that's a legal risk.
- **Do not exceed 4,200 words total.** Target 3,500-4,000. The reviewer fails scripts >4,200.
- **If the topic's row has `approved` = Y in the Sheet, stop and confirm** — that topic is already filmed and the new script may be a refresh.
- **Cite the FILMING LIST tab** if a row exists there for this topic — note its status in the frontmatter `sources_used` block.
