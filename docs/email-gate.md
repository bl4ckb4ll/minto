# Email gate

## Design goal

Do not depend on an agent remembering a writing rule.

The deterministic program owns:

- the exact draft bytes being reviewed;
- the rubric version;
- the model identity and revision;
- the reviewer command;
- validation of the model's output schema;
- the pass/fail policy;
- the receipt;
- verification that the receipt still belongs to the exact draft.

The model owns only semantic classification that is inconvenient to encode mechanically.

## The receipt is the joint

`minto_email_check.py check` hashes the draft and rubric, invokes the reviewer, validates its structured output, applies ordinary deterministic policy, and writes a receipt.

`minto_email_check.py verify` recomputes the hashes and policy.

Changing one byte of the email after review invalidates the receipt.

A downstream step should consume an email only after `verify` succeeds. Do not make “remember to run Minto” an instruction to an agent. Make the verified receipt a required input.

## CI proof

A CI run gives stronger evidence than a checked-in receipt because the platform records the job execution and logs. The eventual model-review job should upload its receipt as an artifact, and any send/publish/finalize job should depend on that job.

For higher assurance, protect the workflow file and required check with repository rules. If an agent may freely modify the gate itself, the agent can of course remove the gate.

## Determinism boundary

A local language model remains a probabilistic/implementation-sensitive component even with greedy decoding. Pin:

- exact model repository and revision;
- exact model artifact or quantized-file hash;
- inference runtime version;
- prompt/rubric hash;
- decoding parameters;
- thread count when reproducibility across runs matters.

The system can guarantee that a particular model invocation occurred on particular bytes and record exactly what it returned. It cannot turn the semantic classifier itself into ordinary deterministic code.

That distinction is deliberate: rigid frame, small soft joint.
