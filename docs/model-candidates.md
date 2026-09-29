# Small local model candidates for the email checker

Start small. The task is narrow semantic classification, not general writing.

## First models to benchmark

### HuggingFaceTB/SmolLM2-360M-Instruct

- About 360M parameters.
- Apache-2.0.
- Small enough to make a useful lower-bound experiment on a CPU runner.
- First candidate: if it handles the rubric reliably, a larger model buys little.

### Qwen/Qwen2.5-0.5B-Instruct

- About 0.5B parameters.
- Apache-2.0.
- Useful second small baseline.
- Compare especially on extracting the actual requested action and distinguishing purpose from supporting commentary.

### Qwen/Qwen3-0.6B

- About 0.6B parameters.
- Apache-2.0.
- Newer small Qwen baseline.
- Worth testing after the two smallest baselines rather than assuming newer/larger is necessary.

### meta-llama/Llama-3.2-1B-Instruct

- About 1B parameters.
- Meta Llama 3.2 license, not Apache-2.0.
- Useful as a larger reference point if sub-billion models fail.
- Licensing and gated-download ergonomics make it less attractive for an unattended GitHub Actions baseline.

## Benchmark before choosing

Build an email fixture set with known expected classifications. Include:

- request first, explanation second;
- praise/analogy first, request later;
- informational email with no requested action;
- reply whose controlling thought is an answer rather than a request;
- necessary context before a request;
- unnecessary autobiography before a request;
- terse informal email;
- typo-heavy but semantically clear email.

For each model and pinned revision, record:

- exact artifact hash;
- inference runtime and version;
- wall-clock CPU time;
- peak memory if practical;
- exact-schema success rate;
- classification accuracy per field;
- whole-email gate accuracy;
- repeated-run stability.

Do not pick a model from general benchmarks. Pick the smallest model that passes this repository's fixture set reliably.
