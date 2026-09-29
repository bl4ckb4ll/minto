# microsoft/Phi-4-mini-instruct

Hugging Face ID: `microsoft/Phi-4-mini-instruct`

License: MIT.

Role: lower-bound writing/revision model.

The full Hugging Face repository is roughly 7.7 GB. This model is included to determine whether a much smaller writer can satisfy the Minto acceptance cases, not because small size is itself the target.

Questions to measure:

- Can it make a structural correction without flattening the sender's voice?
- Can it preserve all content while making only a minimal edit?
- Where does it fail relative to the 9B and 12B candidates?
- Can it serve as a cheap first-pass rewriter while a larger model handles difficult cases?

A pass on the semantic checker does not qualify it as a writer.
