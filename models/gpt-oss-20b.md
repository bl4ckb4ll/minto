# openai/gpt-oss-20b

Hugging Face ID: `openai/gpt-oss-20b`

License: Apache-2.0.

Architecture note: about 21B total parameters with about 3.6B active parameters per token.

Role: larger / MoE reference model for Minto revision.

Use it after the smaller writing candidates establish a baseline. Parameter count is not directly comparable with dense 9B or 12B models, so the experiment should compare actual editing behavior, latency, memory use, and retained receipts rather than model size.

Important runtime note: the model expects OpenAI's harmony response format. Preserve that detail in the runner rather than treating it as an interchangeable plain chat model.

Questions to measure:

- Does it resolve hard structural cases that the dense candidates miss?
- Does reasoning improve minimal editing, or merely encourage more rewriting?
- Does it preserve voice and factual content better enough to justify the extra runtime complexity?
