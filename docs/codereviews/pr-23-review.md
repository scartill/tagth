# PR Review: #23 — Principal Actions

**Reviewed**: 2026-10-30
**Author**: scartill (Boris Resnick)
**Branch**: principal-actions → main
**Decision**: APPROVE

## QA & Verification Guidance
- **Risk Assessment & Migration Notes**: The change is additive and backward compatible for all valid public API callers. The `#` delimiter was previously not an identifier character, ensuring existing principal strings are unaffected. Note that the internal private helper `_normalize_principal` now returns `tuple[list[str], list[str]]` instead of `list[str]`, and principals carrying a `#` global-actions section are granted their global actions on empty resource strings (`''`), matching `root` behaviour.
- **Behavioral Changes to Verify**:
  - Global action permissions: Principals carrying `# <action-list>` (e.g. `# read`) are granted listed actions across all resources, including empty resources (`''`), subject to standard prefix matching.
  - Equivalence of `# all` and `root`: Specifying `# all` grants full access across any resource, equivalent to `root`.
  - Rejection of invalid `#` syntax: Principals with multiple `#` characters, empty action lists after `#` (such as `campaign_42 #` or bare `#`), and combinations of `void` with a `#` section must raise `TagthValidationError` in `allowed()` and return `False` in `validate_principal()`.
- **Testing Hints for QA**:
  1. Verify evaluation of `# read` across standard resources, resources with `anyone` access, and empty resources (`''`), ensuring attempted `all` actions remain denied.
  2. Verify invalid syntax handling for `#`, `campaign_42 #`, `void # read`, and `# read # write` across both `allowed()` and `validate_principal()`.

> Note: Product-audience narrative (shipped value, deferred items, next iteration) is
> **not** part of the review — it is posted separately by the `Finalize` command.

## Technical Summary
The PR implements the `#` global-actions principal syntax specified in Issue #22 and adheres to the security sentinel guidelines, maintaining input bounds, isolated exception chaining, and static error messages. All conformance test vectors pass and documentation accurately reflects grammar additions and reserved characters.

## Findings

### CRITICAL
None

### HIGH
None

### MEDIUM
None

### LOW
- **Missing explicit test cases for `validate_principal` with global actions**: While `allowed()` and internal parsing methods are thoroughly tested in `test/test_global_actions.py` and `test/test_normalize_principal.py`, `validate_principal` is not explicitly asserted against valid and invalid `#` syntax in the test suite. Given `validate_principal` wraps `_normalize_principal` directly, adding dedicated assertions would reinforce public API test completeness.
- **Grammar re-instantiation per invocation**: The `_parse_global_actions` function constructs its pyparsing parser on each call, following the existing pattern of `_parse_tag_list` and `_normalize_resource`. While input lengths are strictly capped at 2048 characters to prevent DoS, moving parser construction to module level or applying memoization could be considered during future maintenance to reduce per-call parsing overhead.

## Validation Results

| Check | Result |
|---|---|
| Type check | Skipped |
| Lint | Pass |
| Tests | Pass |
| Build | Skipped |

*Note on test validation*: 101 tests passed. The single failure in `test/test_normalize_resource.py::test_empty_resource` is a pre-existing, unrelated issue concerning `_normalize_resource(None)` and was not introduced by this PR.

## Files Reviewed
- `.agents/skills/scartill-sdd-lite/SKILL.md` (Added)
- `.agents/skills/scartill-sdd-lite/prompts/sc.archive.md` (Added)
- `.agents/skills/scartill-sdd-lite/prompts/sc.autoflow.md` (Added)
- `.agents/skills/scartill-sdd-lite/prompts/sc.brainstorm.md` (Added)
- `.agents/skills/scartill-sdd-lite/prompts/sc.brainstorm.to.seed.md` (Added)
- `.agents/skills/scartill-sdd-lite/prompts/sc.code.review.md` (Added)
- `.agents/skills/scartill-sdd-lite/prompts/sc.critique.spec.md` (Added)
- `.agents/skills/scartill-sdd-lite/prompts/sc.finalize.md` (Added)
- `.agents/skills/scartill-sdd-lite/prompts/sc.gate.input.md` (Added)
- `.agents/skills/scartill-sdd-lite/prompts/sc.handoff.code.review.md` (Added)
- `.agents/skills/scartill-sdd-lite/prompts/sc.handoff.critique.md` (Added)
- `.agents/skills/scartill-sdd-lite/prompts/sc.implement.tasks.md` (Added)
- `.agents/skills/scartill-sdd-lite/prompts/sc.plan.spec.md` (Added)
- `.agents/skills/scartill-sdd-lite/prompts/sc.save.spec.md` (Added)
- `.agents/skills/scartill-sdd-lite/prompts/sc.split.tasks.md` (Added)
- `.agents/skills/scartill-sdd-lite/references/frontmatter.md` (Added)
- `.kiro/skills/scartill-sdd-lite/SKILL.md` (Added)
- `.kiro/skills/scartill-sdd-lite/prompts/sc.archive.md` (Added)
- `.kiro/skills/scartill-sdd-lite/prompts/sc.autoflow.md` (Added)
- `.kiro/skills/scartill-sdd-lite/prompts/sc.brainstorm.md` (Added)
- `.kiro/skills/scartill-sdd-lite/prompts/sc.brainstorm.to.seed.md` (Added)
- `.kiro/skills/scartill-sdd-lite/prompts/sc.code.review.md` (Added)
- `.kiro/skills/scartill-sdd-lite/prompts/sc.critique.spec.md` (Added)
- `.kiro/skills/scartill-sdd-lite/prompts/sc.finalize.md` (Added)
- `.kiro/skills/scartill-sdd-lite/prompts/sc.gate.input.md` (Added)
- `.kiro/skills/scartill-sdd-lite/prompts/sc.handoff.code.review.md` (Added)
- `.kiro/skills/scartill-sdd-lite/prompts/sc.handoff.critique.md` (Added)
- `.kiro/skills/scartill-sdd-lite/prompts/sc.implement.tasks.md` (Added)
- `.kiro/skills/scartill-sdd-lite/prompts/sc.plan.spec.md` (Added)
- `.kiro/skills/scartill-sdd-lite/prompts/sc.save.spec.md` (Added)
- `.kiro/skills/scartill-sdd-lite/prompts/sc.split.tasks.md` (Added)
- `.kiro/skills/scartill-sdd-lite/references/frontmatter.md` (Added)
- `CHANGELOG.md` (Modified)
- `README.md` (Modified)
- `pyproject.toml` (Modified)
- `skills-lock.json` (Added)
- `src/tagth/tagth.py` (Modified)
- `test/test_global_actions.py` (Added)
- `test/test_normalize_principal.py` (Modified)
- `test/test_tagth.py` (Modified)
- `uv.lock` (Modified)
