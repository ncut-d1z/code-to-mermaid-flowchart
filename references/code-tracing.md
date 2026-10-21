# Trace actual execution

Inspect implementation and relevant local instructions first. Locate entry functions and registrations using repository search, then follow dispatch tables, wrappers, defaults, strategy flags, helper calls, exceptions and all return sites. Read enough callers to identify effective arguments rather than relying on a function signature alone. Do not infer behavior from names, papers, README text or old diagrams.

Record inputs/observations, validation and filtering, initialization and initial-guess sources, core calculations, external calls, iteration state and update order, convergence tests, exact comparison operators, iteration bounds, numerical failures, fallbacks, outputs and status flags. Distinguish success, early success, invalid input, nonconvergence, numerical failure and exhausted iterations only where code actually distinguishes them. An uncaught exception is not an invented graceful failure branch. Preserve short-circuit ordering when it affects execution.

For every meaningful node and edge, record file, symbol and verified line range. A shared helper can have its own diagram and provenance. Record actual Git SHA, worktree modifications and file hashes; line numbers alone become stale. If an execution path depends on unresolved runtime dispatch, state what is unknown and the evidence needed. Static analysis is useful, but is not runtime coverage.

## Machine-readable evidence contract

Use JSON with this structure (replace all example values with observed facts):

```json
{
  "commit": "full observed Git SHA or null for non-Git inputs",
  "analysis": "static",
  "dirty": false,
  "algorithms": [{
    "id": "solver-checked",
    "diagram": "docs/solver.mmd",
    "entry": "src/solver.py:solve",
    "calls": ["src/backend.py:factor"],
    "nodes": ["input", "valid"],
    "edges": ["input-valid"],
    "evidence": [{
      "kind": "node",
      "id": "input",
      "file": "src/solver.py",
      "symbol": "solve",
      "start": 12,
      "end": 14,
      "sha256": "observed file SHA256",
      "condition": "input arguments"
    }],
    "uncertainties": []
  }]
}
```

Add evidence for **every** listed node and edge; this abbreviated example deliberately does not represent a complete manifest. Use edge IDs to distinguish multiple branches between the same nodes. Record the exact branch predicate or unconditional transition under `condition`. Paths are repository-relative. `diagram` must identify an existing Mermaid source. `analysis` is `static`, `runtime`, or `mixed`; runtime claims also require commands/logs in the acceptance report. For a dirty worktree set `dirty: true`; hashes bind evidence to actual file contents. For non-Git input use `commit: null` and explain provenance in the report.

The validator checks manifest completeness, hashes, line ranges and current Git provenance. It does not prove that a symbol exists, that diagram IDs match parsed Mermaid, or that the interpretation of code is correct. Compare the parsed diagram and evidence manually or with project-specific tooling. Do not manipulate the manifest to make a failed check pass without retracing the source.
