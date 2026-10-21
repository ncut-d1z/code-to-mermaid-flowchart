---
name: code-to-mermaid-flowchart
description: Generate, audit, and synchronize Mermaid algorithm flowcharts from real source-code execution paths; compare implementation variants and align notation with research papers. Use for code-to-flowchart documentation, diagram/code consistency reviews, algorithm branch comparisons, or Mermaid/KaTeX web integration and export validation. Do not use for numerical solving or performance optimization alone without a diagram task.
---

# Code to Mermaid Flowchart

## Establish scope

1. Select generation, read-only audit, synchronization, web integration, acceptance, or a combination. Preserve read-only scope for audits; report proposed corrections without editing unless requested.
2. Resolve repository, branch/commit, entry points, variants, optional papers, output directory, language, and requested deliverables from the task. Inspect repository instructions and existing conventions. Use reasonable defaults; ask only about material ambiguities.
3. Record the actual source SHA and dirty-worktree state. Do not reset unrelated changes. Record available tooling and pinned Mermaid/KaTeX versions before choosing syntax. Do not install or upgrade dependencies merely to hide incompatibility.
4. Never change solver logic, invoke expensive experiments, alter stored results, add a web application, commit, push, or publish by default. Perform those actions only within the user's authorization. Diagram switching must not invoke numerical solving.

## Execute

1. Read [code-tracing.md](references/code-tracing.md). Trace actual entry points, dispatch, calls, branches, loops, returns and exception handlers. Build node/edge-to-code evidence before drawing. Code controls execution truth; papers control notation only.
2. Read [variant-analysis.md](references/variant-analysis.md). Build a difference matrix and decide which paths can share a diagram. Resolve runtime dispatch where possible; explicitly label unresolved paths and static-only analysis.
3. If mathematics or a paper is involved, read [math-notation.md](references/math-notation.md). Define meanings before symbols and keep paper definitions distinct from implementation names. Do not invent missing notation.
4. Read [mermaid-style.md](references/mermaid-style.md). Produce concise `flowchart TD` diagrams with explicit conditions, loop updates, terminal statuses and double-bordered subroutine calls. Keep explanations outside diagrams.
5. For synchronization, compare the recorded baseline to the target commit, retrace affected callers and variants, and update evidence as well as diagrams. Do not assume a small code diff implies a small control-flow change.
6. For requested web integration or visual acceptance, read [browser-acceptance.md](references/browser-acceptance.md). Reuse existing rendering and test infrastructure; verify pinned versions in a real browser and inspect downloaded artifacts. Otherwise do not add UI or export functionality.
7. Read [deliverables.md](references/deliverables.md). Deliver sources, provenance, variant/notation tables and an evidence-based acceptance report. Run the bundled provenance validator when using its JSON contract; it checks evidence structure, not semantic correctness or Mermaid syntax.

## Resources and validation

- `python scripts/validate-trace.py trace.json --root /path/to/repository`: verify referenced files, actual line ranges, node IDs, edge IDs, source hashes and commit provenance; exits 0 PASS, 1 FAIL, 2 BLOCKED. See the contract in [code-tracing.md](references/code-tracing.md).
- Use the target project's actual Mermaid parser/renderer for syntax. Never substitute regular expressions or the provenance validator for parser execution.
- Use [browser-acceptance.md](references/browser-acceptance.md) for project-specific real-browser and export tests; do not fabricate universal selectors or stub scripts.
- Use [application-example.md](references/application-example.md) only for the optional Spherical-Flow case study; it is not a default repository or authorization to modify it.
- Use [evaluation.md](references/evaluation.md) to evaluate this skill's behavior and triggering. Separate manual evaluation from measured platform auto-selection.
