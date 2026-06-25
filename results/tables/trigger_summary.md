# Trigger Case Summary

This summary is generated from `benchmark/trigger_cases.csv`, which is a
manually constructed trigger-routing benchmark input.

The counts below describe benchmark case composition only. They are not
model accuracy results and should not be interpreted as broad validation or
statistical significance.

## Input Summary

- Total cases: 36
- Case IDs with the `manual-` prefix: 36
- Distinct expected labels: 3
- Distinct relevant skill values: 6

## Counts by Expected Label

| Expected Label | Count |
| --- | --- |
| should_trigger | 15 |
| should_not_trigger | 12 |
| ambiguous | 9 |

## Counts by Relevant Skill

| Relevant Skill | Count |
| --- | --- |
| skill-design-guide | 7 |
| skill-security-guard | 6 |
| persistent-memory | 7 |
| agent-self-audit | 4 |
| lobster-guard | 5 |
| none | 7 |

## Limitations

- Every case is a manually constructed example rather than an observed user log.
- The summary does not measure routing quality until a later execution layer is added.
- `none` denotes cases that should not route to one of the inspected skills.

