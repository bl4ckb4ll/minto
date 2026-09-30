# Rick Baker

This branch is dedicated to Rick Baker, my high-school English teacher, who later taught at a community college. I am not claiming that the system below reproduces his method. The name marks the part of Minto concerned with useful, sometimes severe, criticism of writing rather than automatic praise.

Baker was down on weasel words and bad structure. One recurring exercise was brutally small: write a single paragraph, often the introductory paragraph to a longer essay. A weak paragraph could receive less than half credit. The important lesson for this project is not the number attached to the work. It is that writing improves when criticism identifies what is wrong strongly enough that the writer has to try again.

A score is optional. Diagnosis is not.

## Goal

Rick Baker should act as a critical reader of short prose.

Given a passage, it should help answer questions such as:

- What point is the writer actually trying to get across?
- Which sentences advance that point?
- Which words weaken, blur, hedge, inflate, or accidentally redirect it?
- What does the text explicitly state?
- What does it merely imply or suggest?
- What additional conclusions might a particular reader draw?
- Which of those implications are wanted, and which are collateral damage?
- How could the same underlying material be told differently to a different reader without becoming false?

The target is not a single canonical rewrite. The target is a controlled family of possible rewrites plus criticism of the differences among them.

## First floor: many ways to say it

Very early in the pipeline, generate many ways of getting approximately the same point across.

They should **not** be forced to be exact paraphrases. Small changes of phrasing change presupposition, implication, emphasis, register, confidence, chronology, and the apparent source of knowledge. Those differences are useful data.

For each candidate, preserve at least:

1. the candidate text;
2. the apparent main claim;
3. facts explicitly asserted;
4. presuppositions;
5. conversational implicatures;
6. tone and register;
7. facts or attitudes a reader might infer about the writer;
8. information lost relative to the source;
9. information apparently added by the rewrite;
10. a reverse rendering: what a reader would say the candidate meant.

Then compare the reverse rendering with the writer's intended point.

This is less like finding a single "better sentence" and more like exploring a local space of meanings.

## Forward and reverse maps

A useful abstraction is:

```
source experience / intended point
        ↓
candidate wording
        ↓
reader interpretation
        ↓
reconstructed point
```

We want to inspect both directions.

The mathematical analogy is probably **not** an exact functor. A closer family of ideas is a bidirectional transformation or lens: one representation is transformed into another while we keep asking what information survives, what information is discarded, and what changes when we map back.

The analogy should remain subordinate to the actual language behavior. We should record failures rather than force prose into a category-theoretic shape.

## Example: source of knowledge

Compare:

> My research showed that you need to select your mentor very carefully.

with:

> People told me that you need to select your mentor very carefully.

These can serve a similar rhetorical purpose, but they do not carry the same information.

The first explicitly attributes the conclusion to the writer's research. The second attributes it to other people. The second may still suggest that the writer sought information from knowledgeable people, but that is an implication, not an entailment. It also changes the apparent burden of evidence and the writer's stance toward the claim.

Rick Baker should make distinctions like that visible.

It should not merely say "version B is shorter." It should say what changed.

## Hearers

Run candidate passages through several modeled hearers.

A hearer is not just a demographic label. It is a bundle of expectations, background knowledge, incentives, suspicion, time pressure, and purpose.

Examples:

- a hiring manager skimming a resume;
- a professor deciding whether a student understands a claim;
- a technical peer who wants evidence;
- a skeptical stranger;
- a friendly reader who already knows part of the story;
- a reader who has only one paragraph and no surrounding context.

For every hearer, ask:

- What do they think happened?
- What do they think the writer is claiming?
- What do they think the writer knows directly?
- What do they think is hearsay?
- What do they think has been omitted?
- What do they think the writer wants from them?
- Which phrase is most likely to distract or mislead them?

Different hearers may produce very different readings of the same true text.

## Selection is not lying

A twenty-year period contains far more material than can fit into one paragraph.

A resume, cover letter, research statement, personal history, or answer in conversation may legitimately select completely different parts of the same history depending on the question and the reader. Two truthful tellings can therefore look very different.

Rick Baker should distinguish:

- contradiction;
- omission;
- compression;
- emphasis;
- audience-dependent selection;
- change of viewpoint;
- genuinely incompatible stories.

The system should not treat all variation as dishonesty.

## Criticism before scoring

The project should be able to say that a passage is bad.

But criticism should point to an object.

Bad:

> This paragraph is weak. 3/9.

Better:

> The first sentence promises an explanation of why you did not pursue a PhD. The next two sentences switch to advice about choosing mentors, so the paragraph never states the causal link. Either state that link or remove the setup.

Scores may be useful for experiments, but the core product is actionable criticism.

Possible diagnostic axes:

- structure;
- claim clarity;
- evidence;
- relation between evidence and claim;
- unnecessary abstraction;
- weasel words;
- passive or evasive attribution;
- chronology;
- sentence-to-sentence continuity;
- audience assumptions;
- unwanted implication;
- missing implication;
- compression;
- repetition;
- register;
- confidence calibrated to evidence.

Do not collapse these into a single scalar unless an experiment specifically requires it.

## Model work

Pythia belongs in this project early, not as an afterthought.

The first floor should be runnable with Pythia even if its outputs are crude. That gives us a weak-model baseline and exposes which parts of the task actually require learned language behavior.

Other open-weight models, including gpt-oss, can be used as stronger comparators or teachers.

RAG alone is not the intended architecture. Retrieval can supply examples, style notes, prior critiques, or source material, but the central problem is transformation and interpretation:

- generate alternative formulations;
- infer the meanings and implications they produce;
- model several readers;
- map those readings back toward an intended point;
- criticize drift.

Those are model tasks, not merely retrieval tasks.

## Data shape

An initial training / evaluation record can look conceptually like:

```text
source material
intended point
audience / hearer

candidate A
  explicit claims
  implications
  omissions
  collateral effects
  reverse interpretation
  critique

candidate B
  ...
```

Later we can store pairwise relations among candidates:

```
A preserves claim of B
A strengthens B
A weakens B
A changes evidence source from direct to reported
A adds an implication absent from B
A removes a distracting implication from B
```

This turns paraphrase generation into material for training discrimination, not just a pile of alternate wording.

## Early experiment

Start with short passages: one paragraph or less.

For each source:

1. state the intended point;
2. generate 8–20 materially different candidate formulations;
3. reconstruct the apparent point from each candidate without looking at the original intent;
4. run each candidate through several hearers;
5. compare the reconstructed readings with the intent;
6. identify desired and undesired side effects;
7. produce concrete criticism;
8. revise;
9. repeat.

Keep the whole trace. The disagreements and failed rewrites are training material.

## Success condition

The first useful Rick Baker prototype should be able to take one paragraph and return:

- several substantially different ways of saying it;
- a clear account of how their meanings differ;
- at least two distinct reader interpretations;
- a reverse reconstruction of the intended claim;
- specific criticism of structure and wording;
- one revision that fixes a diagnosed problem without introducing a new one.

If it can only retrieve similar examples or produce generic style advice, it has failed the point of the branch.
