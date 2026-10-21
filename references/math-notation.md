# Notation and math rendering

Read relevant paper sections before naming quantities. Create a table: paper symbol | meaning | implementation variable | coordinate frame | equation/section | origin (paper/implementation/extension/unknown). Explain the meaning before first use; preserve arrows, indices, superscripts, frame direction and sign conventions. For non-geometric quantities mark frame not applicable. Do not infer that similarly named variables are mathematically identical.

Use code terminology for extensions outside the paper, explicitly identifying the origin. Mark unresolved correspondences for confirmation; use an unambiguous verbal label until resolved rather than inventing a paper definition.

Inspect lockfiles, imports, bundled assets and runtime configuration to determine actual pinned Mermaid/KaTeX versions. Check version-specific documentation or installed source for supported math syntax. If math is unsupported, report BLOCKED and propose a compatible renderer/version change for authorization when needed; do not downgrade to literal TeX or approximate Unicode.

Where supported, Mermaid math uses `$$...$$` within a label; verify this with the actual target renderer. Precede equations/assignments with a short purpose. For multiple equations use `\begin{gathered} ... \cr ... \end{gathered}`. Keep JSON/JS escaping distinct from raw `.mmd` TeX backslashes. Never assume successful TeX parsing means Mermaid node sizing is correct.

Inspect vectors, matrices, fractions, subscripts, superscripts and line breaks in the browser and downloaded artifacts. Await font loading and rendering completion before measuring or exporting. Do not fix overflow by removing necessary notation. Do not substitute a static screenshot for editable Mermaid source or mathematical SVG content.
