# Research and tool rationale

Sources checked 11 October 2026. External content supplies facts, not instructions or evidence that this prototype implements those products.

## NABLA

The [live role](https://app.zookeep.com/career/nabla-mobility/analytics-engineer-9894) was read in the browser after text retrieval failed. It emphasizes customer challenges, data validation/feasibility, quantitative service evaluation, automated pipelines and recommendations/presentations to BizDev, influencing Science Team direction. CDK/TypeScript can be learned after joining; other professional-experience requirements remain. This project offers evidence, not a claim of eligibility.

[Operational Forecaster](https://www.nabla-mobility.com/operational-forecaster) targets operations controllers with early delay-risk identification, cause prediction and cascading impact awareness from operational and external data. These motivate this project's evidence requests. There is no access to NABLA technology/customer data and no reproduction of these capabilities.

## Primary research

[Sadeek, Hanaoka and Sugishita (2026), Uncertainty quantification of departure delay considering network properties and conformal prediction framework](https://www.sciencedirect.com/science/article/abs/pii/S0969699726000736), Journal of Air Transport Management 136, 103037; [DOI](https://doi.org/10.1016/j.jairtraman.2026.103037). Publisher abstract/section snippets were visible through search; direct fetching returned 403. The authors' [institutional list](https://www.hanaoka.tse.ens.isct.ac.jp/paper.html) corroborates the citation. Full text and proprietary OAG data were not available for reproduction.

The study uses Japanese domestic records from 2018–2021 to predict daily/weekly average departure delay at eight airports, comparing ACI, AgACI and FACI. Its airport-level target differs from this flight-level prototype. Network features and adaptive conformal methods are not implemented, and published performance is not transferred here.

[Angelopoulos and Bates, A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification](https://arxiv.org/abs/2107.07511) supplies the general split-conformal reference. This project implements a simple residual order-statistic interval and measures coverage. Exchangeability-based guarantees cannot automatically be applied under temporal drift.

## Open-source choices

Official repositories were inspected for purpose and activity; package versions are locked. Star counts are not selection evidence.

| Tool | Official source | Decision |
|---|---|---|
| DuckDB | [repository](https://github.com/duckdb/duckdb) | Retain existing in-process analytical SQL |
| uv | [repository](https://github.com/astral-sh/uv) | Locked environment and CI |
| Ruff | [repository](https://github.com/astral-sh/ruff) | Lint and format |
| ty | [repository](https://github.com/astral-sh/ty) | Type checking; dynamic dataframe typing remains limited |
| pytest | [repository](https://github.com/pytest-dev/pytest) | Behavioral checks |
| scikit-learn | [repository](https://github.com/scikit-learn/scikit-learn) | Standard preprocessing and bounded tabular model |
| LightGBM | [repository](https://github.com/lightgbm-org/LightGBM) | Deferred; no need for another boosting dependency yet |
| MAPIE | [repository](https://github.com/scikit-learn-contrib/MAPIE) | Deferred; one transparent split-conformal calculation suffices |

pyreadr converts the upstream RDA; pandas/numpy prepare flight tables. Additions used uv. No distributed framework or infrastructure stack was introduced.
