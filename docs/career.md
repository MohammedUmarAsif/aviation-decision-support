# CV and interview drafts

These describe completed artifacts with AI assistance. Personal review of implementation and recommendations remains pending. No independent coding, mastery or production claims are made.

## Three CV bullets

- Developing an independent, AI-assisted aviation decision-support prototype using Python and DuckDB; its validated diagnostic pipeline audits 1,806 BTS carrier-airport records covering 697,754 reported flights, documents missing counts and flags 19 cause-reconciliation discrepancies.
- Extended the prototype with an AI-assisted retrospective departure-delay experiment on 336,776 public NYC flight records, comparing a median baseline with a random forest using chronological validation, fixed-capacity alerts and empirical conformal coverage; reported model underperformance and uncertainty limits.
- Packaged the analytical workflow with locked uv dependencies, behavioral pytest checks, Ruff/type checks, Docker and GitHub Actions; documented stakeholder recommendations, source provenance and an explicit AI contribution and personal-learning record.

Use CI wording with the final validation record. These are artifact claims, not proof the owner can yet explain every implementation choice.

## Sixty-second interview draft

“I'm developing an independent aviation decision-support prototype with AI assistance. The question is which airline-airport segments deserve investigation and what evidence would justify action. The monthly audit covers roughly 698,000 reported flights. Delta–Atlanta has the largest total delay burden, but a lower delay rate than some smaller segments, so the metric changes the priority. The pipeline flags missing counts and inconsistent cause totals.

I extended it with a historical flight-level experiment. The simple baseline beat the random forest on average error, and uncertainty intervals fell below their coverage target. My recommendation is to request current schedule snapshots, rotation data and decision-time weather before considering operational use. One concept I have checked is that a lower delay percentage can still mean more late flights when traffic is larger. I'm still learning Python and reviewing the AI-generated methods; I don't claim production readiness or airline savings.”
