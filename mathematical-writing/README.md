# Mathematical writing

This branch is for studying and improving mathematical exposition.

The goal is not to define one canonical style. Good mathematical writing can be terse, discursive, geometric, computational, historical, conversational, or formal. The useful question is: what changes make a piece of mathematics easier to enter, follow, remember, and reuse without damaging the mathematics?

## Main objects

- `reference-writers.md` — writers and books worth studying, including mixed cases.
- `repair-types.md` — classes of writing repairs, from local edits to reordered "sub-books".
- `pairs/` — paired source/rewrite examples when redistribution permits, or paraphrased structural examples when it does not.
- `remix-policy.md` — attribution and provenance rules for reorganized or rewritten source material.

## Basic unit

Prefer paired material:

1. source or faithful structural description;
2. diagnosis;
3. revised version;
4. what changed;
5. what was preserved;
6. uncertainty / possible loss.

The corpus should contain both positive and negative examples from the same writer when possible. Avoid turning authors into labels for "good" or "bad" writing.

## Mock emitter

`mock-emitter` is deliberately fake transformation logic for exercising the end-to-end text path on SDF before a real mathematical-writing model exists.

It reads plain text from standard input (or optional file arguments). For inputs longer than five lines it emits:

1. the first line;
2. three distinct random interior lines, kept in their original source order;
3. the final line.

Inputs of five lines or fewer pass through unchanged.

The implementation uses only POSIX `/bin/sh` and `awk`, creates no temporary files, and has no GNU-specific dependency.

```sh
printf '%s\n' one two three four five six seven eight | ./mathematical-writing/mock-emitter
./mathematical-writing/mock-emitter < draft.txt
```

The stdin → stdout contract is the part intended to survive. The line-selection behavior is only a mock replacement for future rewrite logic.

## Long-range use

The corpus is intended to support training/evaluation of systems that revise mathematical prose. It should therefore preserve the operation performed: local clarification, notation repair, dependency repair, section reordering, pruning, through-line extraction, or broader stylistic rewrite.
