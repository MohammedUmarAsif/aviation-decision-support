# Public page validation and release plan

Prepared 12 October 2026 for the implementing agent. Current status: **implemented, published and verified**. See [UI validation and release evidence](UI_VALIDATION.md). The plan below remains the reproducibility/release contract; completion does not imply personal review of all AI-generated methods.

## Why GitHub Pages

The requested artifact is an interactive presentation of reproducible saved research. GitHub Pages serves HTML/CSS/JavaScript from a repository and can deploy via Actions. It does not run the Python training pipeline or a live inference server. The pipeline produces reviewed evidence files before publication.

Official references:

- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

The intended default project URL is https://mohammedumarasif.github.io/aviation-decision-support/. GitHub API reported no Pages site at preparation time. Enable Pages for the existing repository during the authorized implementation/publishing stage, then return the URL actually reported by deployment and verified in the browser.

## Bounded releases

### A. Export defensible evidence

Add the monthly complete-aggregate and measured capacity-grid exports specified in SOL.md. Record public scope, hashes, counts and experiment settings. Use a schema version and explicit study IDs to prevent mixing 2026 arrival aggregates with 2013 departure forecasts. Preserve the original frozen metrics and raw files. A pipeline change is justified only to support a real evidence need.

Run:

```powershell
uv sync --locked --python 3.12
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run python -m pytest -q
```

Run the relevant analysis/export once after changes. Retain existing research reproduction checks and compare capacity-20 results. Store public report reconciliation results. If real BTS raw input is unavailable in CI, use committed derived aggregates with hashes plus meaningful synthetic tests; do not publish raw files or pretend CI independently re-acquired BTS data.

### B. Implement and inspect the story

Create site files with native, accessible controls. Serve locally and test the default view, each ranking, segment selection, model selection, every capacity value, disclosures, brief export, URL restore, reset, loading failure and source links.

Use the documented browser tooling for actual rendering. Save screenshots at 1440×900 and 390×844, and check 320px width for overflow. Reset browser viewport overrides. Record observed visual results, keyboard navigation, focus visibility, chart labels, touch targets and contrast. Do not claim mobile/desktop validation from source inspection alone. A static data chart is not an invented screenshot; all plotted values must reconcile to exports.

Useful success criteria:

- Initial page explains the problem and study scope without any interaction.
- A reader can follow problem → data → method → result → recommendation in about three minutes.
- Method details stay accessible without repeating the main story.
- Every analytical number comes from the evidence bundle or is explicitly labeled an explanatory example.
- Review capacity changes actual recorded counts and corresponding interpretations.
- No current-operation, aviation-safety, causal-benefit or affiliation claims.
- No arbitrary composite data-readiness score or invented model-confidence percentage.
- No raw dataset, CV, credentials or private artifact enters the export/build context.

### C. Publish a verifiable release

Preserve unrelated work and inspect the staged file list. Commit the page and relevant pipeline/evidence changes; do not rewrite prior history. Add a dedicated Pages workflow with only required permissions. The build/validation job must finish successfully before deployment; use the official configure-pages, upload-pages-artifact and deploy-pages tools/workflow pattern after checking current docs. Upload only the reviewed site directory, not the entire repository.

When using a deployment workflow, configure repository Pages to use Actions. Keep existing analytical CI. Wait for required checks and the deployment result, then verify the public URL by HTTP and actual browser rendering. Check asset paths under the repository subpath, interaction state on refresh, downloaded brief and source links. A successful push alone is not publication evidence.

Write docs/UI_VALIDATION.md with observed sizes, tested interactions, evidence revision, CI/deployment URL and outstanding limits. Update README with the verified live link, screenshot, short research story and reproduction instructions. Add the website field to GitHub repository metadata if appropriate. Record implemented/experimental/planned status and preserve personal review boundaries.

### D. CV and researcher entry points

CV label after verified publication: **Aviation Decision Support — Interactive Research Study**. Link that phrase to the live Pages root rather than a long parameterized URL. Keep code as a secondary link on the page.

Use a brief project description based on completed work: independent, AI-assisted analysis of delay burden and forecast review usefulness with reproducible evidence. Do not rename it as an airline-deployed product or claim the owner independently authored all code.

Researchers should find methodology, data dictionary, research sources, public evidence manifest, machine-readable aggregates, tests and CI in one evidence section. Recruiters should understand the problem and result before encountering these artifacts.

## Owner learning checkpoints

1. Rate, traffic and minutes: explain why the ranking changes when the objective changes.
2. Chronology and features: identify a post-event field and why it cannot be used at planning time.
3. Error and review capacity: explain why lower average error does not necessarily mean more severe delays found in a small queue.
4. Coverage and scope: explain what December undercoverage and dated NYC data prevent us from claiming.
5. Reproduction: run one pipeline command, change one display choice, and trace its value back to evidence.

Record actual answers only. These can proceed during implementation; they do not require stopping authorized build work or fabricating approval.
