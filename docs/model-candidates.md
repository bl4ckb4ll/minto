# Local model candidates for Minto email review

The model choice depends on the job. Keep **classification** and **rewriting** separate.

The deterministic envelope should never depend on a model deciding whether its own work passes. Models emit semantic facts or candidate revisions; ordinary code applies policy and verifies the exact bytes.

## 1. Semantic checker

The checker answers narrow questions such as:

- What is the purpose of this email?
- Is the purpose in the opening?
- Does supporting commentary precede the purpose?
- What action is the recipient being asked to take?
- Is that action explicit?

For this job, very small models remain worth testing because the output schema is tiny and the task is classification rather than prose generation.

### Lower-bound candidates

- **HuggingFaceTB/SmolLM2-360M-Instruct** — 360M, Apache-2.0.
- **Qwen/Qwen2.5-0.5B-Instruct** — 0.5B, Apache-2.0.
- **Qwen/Qwen3.5-2B** — current small Qwen-family comparison, Apache-2.0.
- **microsoft/Phi-4-mini-instruct** — useful larger checker / lower-bound rewriter; MIT.

A tiny checker is useful only if it passes the fixture set. Its size is not itself a virtue.

## 2. Writing / revision model

Rewriting is a harder task. The model has to understand purpose and hierarchy while preserving the sender's voice rather than replacing it with generic polished prose.

Do **not** make the sub-billion checker candidates the default rewriters.

### Primary candidates

#### Qwen/Qwen3.5-9B

- Apache-2.0.
- Current Qwen3.5 dense model.
- Strong first target for the actual revision experiment: large enough to test real prose judgment without immediately jumping to a model that is awkward on a standard CPU runner.
- Full weights are larger than the disk on a standard public GitHub Linux runner, so use a pinned text-only quantized artifact for CI.
- A Q4-class text-only GGUF is roughly 5–6 GB depending on quantizer.

#### google/gemma-4-12B-it

- Apache-2.0.
- Current instruction-tuned Gemma 4 12B.
- Good second writing candidate and a useful test of whether 12B materially improves voice preservation and structural revision over 9B.
- Full weights are about 24 GB.
- ggml-org publishes a Q4_0 GGUF around 7.2 GB, which is practical enough to benchmark on the 16 GB RAM / 14 GB disk public Linux runner.

#### openai/gpt-oss-20b

- Apache-2.0.
- 21B total parameters with 3.6B active parameters.
- Treat as an upper reference rather than the first CI default.
- Its MoE structure makes parameter count less directly comparable with dense 9B/12B models.
- Benchmark only after the smaller writing candidates so we know whether the extra machinery buys anything on this task.

### Secondary lower-bound rewriter

#### microsoft/Phi-4-mini-instruct

- MIT.
- Much smaller download than the 9B/12B candidates.
- Worth including to locate the quality cliff: can it make a structurally correct edit without flattening the writer's voice?
- Do not assume success merely because it follows the rubric.

## 3. Proposed pipeline

```
raw draft
    |
    v
semantic checker
    |
    v
deterministic policy
    |
    +---- pass --------------------------+
    |                                    |
    +---- fail --> writing model         |
                       |                 |
                       v                 |
                  revised draft          |
                       |                 |
                       +--> checker ------+
                                |
                                v
                         deterministic policy
                                |
                                v
                      receipt for exact bytes
```

The writing model proposes. The checker classifies. Code decides.

A revision model must not be allowed to silently invent facts, remove substantive qualifications, or replace the writer's voice merely to make the prose more conventional.

## 4. Writing-specific fixture set

The earlier classification fixtures are not enough. Add paired drafts with a human-approved revision and score at least:

- controlling thought moved to the opening;
- request preserved exactly;
- factual content preserved;
- uncertainty preserved;
- writer's characteristic wording preserved when it is not obstructing the reader;
- no generic corporate filler added;
- no unnecessary apology added;
- no praise expanded beyond the original;
- no extra claims or motives invented;
- informal email remains informal;
- typo-heavy but intelligible input gets corrected without being rewritten wholesale;
- minimal-edit instruction actually produces a minimal edit;
- a draft that already passes remains nearly unchanged.

Use the Pythia email as a regression case: the checkpoint request belongs immediately after the thank-you; the GDB analogy is supporting commentary and belongs later.

## 5. Evaluation

For each pinned model artifact and runtime, record:

- exact model and artifact hash;
- quantization;
- runtime version;
- prompt/rubric hash;
- decoding settings;
- wall-clock CPU time;
- peak memory;
- exact-schema success rate for checker mode;
- classification accuracy per field;
- whole-email gate accuracy;
- semantic preservation in revisions;
- voice-preservation score from the fixture expectations;
- edit distance from the input when minimal editing was requested;
- repeated-run stability.

Do not select a writing model from general benchmarks. Select it from this repository's email cases.

## 6. GitHub runner constraint

As of September 2026, a standard public-repository GitHub Linux runner provides 4 CPUs, 16 GB RAM, and 14 GB SSD. That makes quantization part of the experiment rather than an afterthought.

The first serious writing comparison should be:

1. Phi-4-mini-instruct as a lower bound;
2. Qwen3.5-9B at a pinned Q4-class text-only quantization;
3. Gemma-4-12B-it Q4_0;
4. gpt-oss-20b only if the smaller candidates leave a clear quality gap.
