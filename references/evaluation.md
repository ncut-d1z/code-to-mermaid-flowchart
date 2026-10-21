# Skill evaluation cases

Use independent fresh sessions with only the skill and task-local source artifacts when available. Do not give expected findings to the executing agent. Evaluate outputs afterward against actual code. Keep temporary test artifacts outside the skill. Never modify live projects for evaluation.

Positive selection cases:
- “Read this Python/C++ implementation and draw its Mermaid algorithm flowchart.”
- “Audit this existing flowchart against the current source without changing files.”
- “Compare checked/legacy variants with different constraints and document their flows.”
- “Integrate these Mermaid diagrams in our workbench and verify SVG/PNG downloads.”
Negative selection case:
- “Optimize this numerical solver's runtime.” (No diagram request.)

Check mode selection, source evidence, variant separation, call boundaries, failure semantics, notation provenance, real versus claimed tests and nonmutation of read-only inputs. Add a source change and test synchronization against a recorded baseline. Include invalid-input and numerical-failure branches in the fixture.

These are evaluation prompts, not an auto-trigger test harness. If platform skill-selection telemetry is unavailable, report automatic trigger accuracy BLOCKED; a manual metadata review or explicitly invoking the skill cannot establish automatic selection accuracy.
