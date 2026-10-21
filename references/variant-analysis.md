# Decide diagram reuse from execution

Create a matrix with rows for actual algorithm IDs and columns for entry/dispatch, input filtering, initial guess, constraints, solver/backend, update order, iteration budget, convergence, failure/fallback and diagram ID. Cite source locations for each substantive difference.

Use separate diagrams when initialization, constraints, solver strategy, backend steps, stopping rules or failure semantics change. A common outer caller can call distinct subroutine diagrams; retain explicit selection branches and identify which variant is used. Do not hide different semantics behind an undifferentiated “solve” node.

Share only when executable steps and branch meanings are substantively identical. Numerical tolerances, logging and display settings alone need not duplicate diagrams, but document their values or parameterization outside the graph. A parameter that selects an algorithmic branch is a strategy, not merely a number.

For audits, classify each difference as missing step, incorrect condition/order, missing termination, wrong call boundary, conflated variant, invented behavior or stale provenance. Include source evidence, consequence and proposed correction. For synchronization, retrace changed callees and affected callers, not just lines in the diagram file.
