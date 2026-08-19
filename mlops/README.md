# ML/LLMOps Directory Contract

Issue #7 owns this plane after #2 freezes the shared service/artifact/evidence contracts.

```text
mlops/
├── eval/
├── registry/
├── prompts/
├── models/
└── adapters/
```

No model/runtime presence is PASS without an exact run receipt. Model artifacts keep separate digest/license identity from runtime libraries.
