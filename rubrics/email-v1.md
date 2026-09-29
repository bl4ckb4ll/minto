# Email review rubric v1

The reviewer classifies the draft. It does not decide whether the draft passes.

Return one JSON object with exactly these semantic fields:

- `message_kind`: one of `request`, `informational`, `reply`
- `purpose`: a short statement of why the sender is writing
- `purpose_in_opening`: boolean
- `support_before_purpose`: boolean
- `opening_context_sufficient`: boolean
- `writer_centered_before_purpose`: boolean
- `requested_action`: a short string, or null when no action is requested
- `requested_action_explicit`: boolean

Interpretation:

- The opening means the first substantive paragraph after the greeting.
- The purpose should tell the recipient what the message is about before secondary explanation, praise, analogy, autobiography, or argument.
- Supporting material belongs after the controlling thought unless the recipient truly needs it to understand the controlling thought.
- Writer-centered material is material placed for the writer's benefit rather than because the recipient needs it at that point.
- For a request, the action/question must be explicit enough that the recipient can tell what response or action is wanted.
- Do not rewrite the email.
- Do not judge tone, grammar, spelling, politeness, or style except where they obscure the purpose.

This rubric operationalizes the repository's reader-first principle and the Minto practice of putting the controlling thought first.
