# Minto model set

These are the current local-model candidates for Minto email checking and revision.

Large model weights do not belong in this Git repository. Keep exact model IDs, revisions, hashes, quantization, runtime settings, and benchmark receipts here; fetch weights into a content-addressed store or the runner workspace.

Training and qualification work belongs on the `minto` branch of [fuego-ironworks/gym](https://github.com/fuego-ironworks/gym/tree/minto).

## Writing / revision candidates

- [Qwen/Qwen3.5-9B](qwen3.5-9b.md)
- [google/gemma-4-12B-it](gemma-4-12b-it.md)
- [openai/gpt-oss-20b](gpt-oss-20b.md)
- [microsoft/Phi-4-mini-instruct](phi-4-mini-instruct.md)

The first three are the larger writing candidates. Phi-4-mini-instruct remains a lower-bound rewriter so we can locate the quality cliff instead of assuming model size from the outset.

## Acceptance target

A useful Minto writing model should:

1. identify the controlling thought and requested action;
2. move them earlier when needed;
3. preserve facts, uncertainty, and qualifications;
4. preserve the sender's voice;
5. make the smallest useful edit;
6. avoid generic corporate filler;
7. avoid inventing motives or content;
8. leave a draft that already passes mostly unchanged.

The deterministic checker remains authoritative for pass/fail.
