# Qwen/Qwen3.5-9B

Hugging Face ID: `Qwen/Qwen3.5-9B`

License: Apache-2.0.

Role: primary dense writing/revision candidate.

Why it is here:

- large enough to test real prose judgment rather than only semantic classification;
- still small enough to benchmark in quantized form on ordinary CI hardware;
- good candidate for testing whether Minto-style structural editing can preserve an informal personal voice.

Questions to measure:

- Does it move the request or controlling thought earlier without rewriting the whole email?
- Does it preserve unusual but intentional phrasing?
- Does it avoid making prose more corporate than the source?
- Does it obey minimal-edit instructions?
- Does it preserve every factual qualification?

Do not record a capability claim until Gym has a retained receipt for the corresponding acceptance cases.
