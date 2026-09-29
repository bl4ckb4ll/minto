# google/gemma-4-12B-it

Hugging Face ID: `google/gemma-4-12B-it`

License: Apache-2.0.

Role: second major writing/revision candidate and larger dense comparison.

The upstream repository is roughly 24 GB in full precision, so CI experiments should use a pinned quantized artifact rather than fetch the original weights blindly.

Questions to measure:

- Does 12B materially improve voice preservation over the 9B candidate?
- Does it make fewer unnecessary edits?
- Does it better distinguish necessary context from writer-centered preamble?
- Does it preserve terse or blunt email style instead of smoothing it away?

Keep exact quantized-file hash and runtime settings with every retained result.
