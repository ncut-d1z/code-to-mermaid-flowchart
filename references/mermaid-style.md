# Mermaid structure and labels

Use `flowchart TD` by default. Use stable ASCII node IDs and quote labels. Keep a node to one operation or decision; split independent operations. Use diamonds for decisions and label outgoing edges with yes/no or exact mutually exclusive outcomes. Make loop initialization, state update, back edge and exit explicit. Preserve check-before-update versus update-before-check and exact iteration bounds.

Represent external algorithms/modules with double-bordered subroutine nodes, for example `solve[["Call checked solver"]]`. Keep implementation details in the callee's own diagram. Show returned status checks in the caller if present. Never invent a callable subroutine to deduplicate an inline code block. If splitting an inline block for readability, label it explicitly as a diagram continuation, use ordinary connector nodes, and retain source ownership; reserve double-bordered calls for actual code calls. Do not turn every arithmetic primitive into an external call. Label terminal outputs/statuses precisely.

Keep citations, version information, assumptions and long explanations outside the diagram. Split large diagrams by genuine call boundaries, not by omitting logic. Reduce crossing edges without changing order. Do not rely on color alone to communicate outcomes.

For ordinary text line breaks use the project's supported label mechanism, preferring `<br>` where supported and requested. If the delivery renderer prohibits HTML labels, produce the requested project-native source separately and use compatible plain labels in the conversational preview. Do not silently change the artifact's required math or layout semantics.

Run the installed Mermaid parser against every diagram. Record exact version/configuration and invocation. Parser success is not visual or source-fidelity success. Render full-sized diagrams, inspect dense loops and formulas at readable scale, and check bounding boxes and export dimensions. Fix layout without deleting symbols or branches.

Comparisons, assignments and arithmetic copied from code are still mathematical expressions when presented as formulas. Use verified KaTeX or a concise verbal label such as “Below convergence tolerance?” with the exact predicate in the external evidence table. Do not evade math requirements by calling raw formula strings “code labels”.
