# Real-browser and export acceptance

## Prepare a project-specific harness

Use this stage only for requested web integration or applicable visual acceptance. Inspect package/lock files, the actual rendering component, export implementation and existing Playwright/Puppeteer/browser tooling. Reuse their versions and setup. Record browser, renderer, font assets, configuration and commands. If dependencies or a browser are unavailable, report BLOCKED with the concrete missing prerequisite; do not claim a mocked DOM proves browser rendering.

Do not add a web app to a source-only repository. For integration, reuse existing route/tab/components/state. Implement a searchable selector, zoom, fullscreen with selector retained, and Mermaid/SVG/PNG downloads when requested. Limit changes to diagram assets, rendering, selection, export and relevant tests. Avoid large workbench refactors.

## Execute in a real browser

1. Open the real page. Capture page errors and relevant console errors from before load. Wait for application readiness, Mermaid completion and `document.fonts.ready`.
2. Parse/render every algorithm source with the pinned renderer. Verify math is rendered, not exposed as literal TeX. Inspect full diagrams and dense formula/loop regions for clipping, overlap, obscured edges and missing content. Use screenshots as test evidence only.
3. Search/select algorithms; assert selected ID, displayed source and rendered graph agree. Switch between substantively different diagrams and verify the content changes. Test rapid changes to catch stale asynchronous renders.
4. Exercise zoom, enter/exit fullscreen, and switch algorithms inside fullscreen. Ensure controls remain reachable and the full graph can be viewed.
5. Capture each download using actual UI actions. Reparse downloaded Mermaid source and compare with the selected algorithm. Do not validate an unrelated fixture instead.
6. Parse SVG as XML, verify dimensions/viewBox, node/text/math content and absence of missing assets. Check computed styles, fonts and any `foreignObject` dependencies: browser display alone does not guarantee portable SVG. Open exported SVG independently/offline where supported; verify formulas visually. Prefer vector math; do not accept a full-image screenshot embedded in SVG as mathematical SVG export.
7. Decode PNG, check nonzero useful dimensions and inspect the complete image at readable scale. Compare expected labels/formulas and framing with the browser render. PNG is raster: require clear complete math, not editable vector structure. Rasterizing the correctly rendered diagram for PNG is valid; replacing the source or SVG with a screenshot is not.
8. Observe solver requests/events/counters during page load, selection, zoom, fullscreen and export. Assert no numerical solver invocation attributable to diagram actions. Inspect code diff for algorithm/result modifications and use existing targeted regressions if needed; do not run expensive experiments just to prove isolation.

## Report evidence honestly

For each requirement record status, command/action, version, artifact/log and observation. PASS means executed successfully; FAIL means executed and failed; BLOCKED means required but prevented by environment; NOT APPLICABLE means outside the task. Do not mark browser testing PASS based on static inspection or parser-only success. Keep source fidelity, syntax, DOM/math layout, SVG structure/portability and PNG visual correctness as separate results.

Universal UI selectors/export scripts would be misleading across projects. Implement project-local tests using observed selectors and exports, following this checklist; this skill intentionally does not ship placeholder browser or export scripts.
