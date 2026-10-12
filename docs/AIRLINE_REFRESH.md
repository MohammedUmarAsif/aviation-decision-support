# Airline visual refresh, 12 October 2026

Owner request: replace the bright white presentation with an airline feel, add useful visuals and explain the analytical applications with research context.

## Presentation

Midnight navy surfaces, muted blue chart bars and amber caveats retain the original blue/amber identity. The existing result remains in the landing. An airport-at-night illustration adds context immediately below it. Four question-led links lead into reliability, reported workload, review capacity and forecast assurance. A native expandable section explains weather categories, aircraft rotations and airport capacity. No dependencies were added.

The illustration is AI-generated and explicitly labelled. It is not a photograph of an actual airport or evidence of an observed event. See `site/assets/README.md` for provenance. The rotation diagram is a simplified mechanism, not a measured aircraft rotation.

## Research provenance

- [BTS cause definitions](https://www.bts.gov/topics/airlines-and-airports/understanding-reporting-causes-flight-delays-and-cancellations): broad reporting categories; non-extreme weather may appear within NAS delays; late-arriving aircraft can carry delay into subsequent flights. No percentages from this page were imported.
- [FAA delay propagation](https://www.aspm.faa.gov/aspmhelp/index/Delay_Propagation.html): propagation across flight legs can be tracked with the same aircraft's tail number. Rotation-level propagation is a future question, not a result of this study.
- [FAA ground delay programs](https://www.fly.faa.gov/ais/Help/ais_message_help.html): demand exceeding airport acceptance rate provides context for airport-capacity analysis. The page explicitly distinguishes this from the study's daily human review budget.

These sources support explanatory context. No new dataset was acquired, and no passenger, cost, causal, rotation or runway-capacity result is claimed. Evidence JSON, CSV, manifest, models and numerical results are unchanged.

## Verification

- Python suite: 27 tests passed. JavaScript syntax check passed. Diff whitespace check passed.
- Rendered desktop at 1440 x 900; mobile at 390 x 844; narrow mobile at 320 x 740. No horizontal overflow in inspected layouts.
- Reliability entry point selects delay-rate ranking; review-capacity link selects random forest and 40 daily reviews; forecast-assurance link reaches uncertainty. Burden view remains the default.
- Existing native model and capacity controls work: median baseline at 40 daily reviews displays 2,440 reviews, 246 severe delays found and 3,472 missed.
- Native research disclosure expands on mobile. Illustration loads at its intrinsic 1536-pixel width, with its explanatory caption.
- Keyboard Tab reaches navigation with a visible 3-pixel amber focus outline. Native links, selects and disclosures retained.
- No browser warnings or errors observed during the final local interaction check.

Screenshots: `docs/screenshots/airline/`. Earlier light-theme screenshots remain in `docs/screenshots/refresh/` for comparison. Checks are agent execution evidence, not independent human review.
