---
title: "Using Canvas Docs with AI Code Editors"
---

<!-- sources: discussion #615 -->

If you build plugins with an AI-assisted code editor such as Cursor, you can give the assistant access to the Canvas documentation so its suggestions are grounded in the real SDK and FHIR API.

## Context7

The Canvas documentation is published to [Context7](https://context7.com/canvas-medical/documentation), which serves LLM-ready versions of docs to AI code editors. Pointing your editor's Context7 integration at the Canvas documentation lets the assistant pull in current SDK and API reference material while you work.

The underlying [documentation repository](https://github.com/canvas-medical/documentation) is public, which is what makes this indexing possible.

If you try this, coverage will be only as complete as the docs themselves — feedback on where AI-assisted plugin authoring falls short is welcome and helps prioritize documentation work.
