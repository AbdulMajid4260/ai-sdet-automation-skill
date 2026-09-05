---
name: plain-english-playwright
description: Convert plain-English web test steps and a target webpage into maintainable Python Playwright automation using explicit SDET reasoning for locators, synchronization, assertions, ambiguity, dynamic data, failure diagnosis, and validation.
---

# Plain-English Playwright Automation Skill

## Purpose

Convert a user's plain-English web test steps plus a target webpage or flow into working Python Playwright automation. The Skill is not a click-translator: it applies explicit SDET reasoning before producing code.

## Required inputs

1. **Target**: a URL or clearly identified webpage/flow.
2. **Test steps**: ordered plain-English steps describing actions and expected outcomes.
3. **Optional context**: credentials supplied by the user, DOM/accessibility information, expected data, or framework constraints.

If the target or a critical instruction is missing, ask only for the missing information. Never invent a URL, credential, selector, expected value, or application behavior.

## Required output

Return, in this order:

1. A short interpretation of the test.
2. Assumptions and any ambiguities.
3. Locator decisions for important elements.
4. Synchronization decisions.
5. The complete executable Python Playwright test.
6. A short validation checklist.
7. Any limitations or items requiring human verification.

## Step 1 — Parse the natural language

Classify each instruction as one or more of:

- navigation
- data entry
- click/action
- selection
- extraction
- assertion/verification
- dynamic-data operation
- conditional/branching behavior

Separate **actions** from **expected outcomes**. Every meaningful expected outcome should become an assertion where technically possible.

Do not silently convert vague instructions into arbitrary actions.

### Ambiguity rule

If a phrase such as "click the product", "select the item", or "open the account" can match multiple elements and the context does not disambiguate it, stop and request clarification. If the context clearly identifies one element, state the assumption briefly and continue.

## Step 2 — Choose locators using this hierarchy

Prefer stable, user-facing or explicit automation contracts:

1. `get_by_role()` with an accessible name
2. `get_by_label()` for form controls
3. `get_by_placeholder()` when appropriate
4. `get_by_test_id()` when the application exposes `data-testid`
5. stable IDs or dedicated test attributes using `locator()` when the site uses a different explicit attribute
6. stable, meaningful CSS selectors
7. text locators for non-interactive content when appropriate

For repeated components, scope the action to the component containing the requested identity. Example pattern:

```python
product = page.get_by_role("listitem").filter(has_text="Product 2")
product.get_by_role("button", name="Add to cart").click()
```

Avoid:

- absolute XPath
- deep DOM traversal
- generated class names
- `nth-child` when a semantic locator exists
- coordinate clicks
- arbitrary positional assumptions
- hardcoded selectors invented without evidence

If the application provides an explicit `data-test` or similar test contract, it may be preferable to a brittle CSS path. This is especially useful for icon-only controls whose accessible role has no reliable accessible name. Document the reason.

### Locator verification gate

Do not assume that a selector exists merely because it is a common convention, appears in an example, or looks plausible.

Before treating a locator as verified:

1. Prefer inspecting the actual target page, DOM, or accessibility tree when the environment provides browser/page-inspection capabilities.
2. Confirm that the proposed selector matches at least one intended element.
3. For repeated elements, confirm that the locator resolves to the intended component rather than an arbitrary match.
4. Prefer selectors that are both stable and actually observed on the target application.
5. Never invent a `data-testid`, `data-test`, ARIA label, role/name, ID, or CSS class.
6. If the target page cannot be inspected, label selectors as assumptions and avoid claiming that they were verified.
7. If execution reveals that a locator does not resolve, diagnose the actual DOM/locator mismatch before changing unrelated parts of the test.

A selector that is theoretically stable but does not exist on the target page is not a valid locator.

Use these confidence labels when useful:

- **verified locator** — supported by actual DOM/accessibility/page evidence or successful execution evidence.
- **inferred locator** — reasonable but not directly verified.
- **failed locator** — disproven by execution or inspection.

Never describe an inferred or failed locator as verified.

## Step 3 — Synchronization

Use Playwright's locator auto-waiting and web-first assertions. Do not use arbitrary sleeps such as `time.sleep(5)` or `page.wait_for_timeout(5000)` as normal synchronization.

Use explicit waits only when there is a concrete state transition that cannot be expressed with a locator/assertion.

For navigation, prefer waiting through Playwright actions/assertions rather than fixed delays.

## Step 4 — Assertions

Automation must verify outcomes, not merely perform actions.

Use `expect()` assertions for:

- page/heading visibility
- URL or navigation state when relevant
- element visibility
- expected text
- expected count
- selected/checked state
- final business outcome

Assertions should be specific enough to catch a real regression.

## Step 5 — Dynamic data

When a step describes a relative property rather than a fixed value, compute it from the page.

Examples:

- "cheapest product" → inspect product prices, parse numeric values, select minimum
- "first available item" → identify availability explicitly
- "highest rated result" → inspect displayed ratings and compute the maximum

Do not replace a dynamic requirement with a hardcoded item merely because a known demo dataset currently has a predictable answer.

When UI behavior and business-data computation are both part of the requirement, keep them conceptually separate. For example, if the user asks to sort low-to-high and then choose the cheapest product, exercise the sort control as requested while independently deriving the minimum from rendered data when that provides a stronger assertion.

## Step 6 — Code generation

Generate complete executable Python using Playwright's synchronous API unless the user explicitly requests async.

Use pytest when the output is a test case.

Prefer a simple, readable test over a framework-heavy abstraction. Do not create page objects, factories, dependency injection, or utilities unless repeated behavior genuinely justifies them.

Use constants for stable test data such as the target URL and public demo credentials. Do not commit real secrets.

Generated code should be deterministic and reproducible. Avoid unnecessary complexity that does not contribute to the requested test behavior.

## Step 7 — Validation mindset

Before presenting the final answer, review:

- Does every selector correspond to an element that actually exists or has been clearly identified from available page information?
- Was each important locator selected from observed evidence rather than invented from convention?
- Is any selector unnecessarily brittle?
- Are repeated components scoped to the correct item?
- Are dynamic states synchronized?
- Are assertions meaningful?
- Is the test deterministic?
- Are assumptions explicit?
- Are there arbitrary sleeps?
- Is any information hallucinated?
- Can another engineer reproduce the test?

If execution tools are available, execute the generated test against the target environment.

Treat an execution failure as evidence that requires diagnosis, not as a reason to blindly generate another selector.

When a locator fails:

1. Capture the failing selector and error.
2. Determine whether the element exists under another stable selector.
3. Inspect the relevant DOM/accessibility information when available.
4. Replace only the incorrect assumption.
5. Rerun the affected test.
6. Record the failure and correction when it provides useful evidence about the application's structure.
7. Do not claim success until the corrected test actually passes.

Never report a test as passing without execution evidence.

## Step 8 — Failure handling

When a locator or behavior cannot be verified:

1. Do not invent a selector.
2. Explain what is unknown.
3. Use available page/DOM/accessibility information if provided.
4. Ask for clarification only if the missing information blocks reliable generation.

When generated automation fails during execution:

1. Treat the failure as a validation result.
2. Identify the exact failing action, locator, or assertion.
3. Determine whether the failure is caused by:
   - an incorrect locator
   - incorrect synchronization
   - an incorrect assumption about application behavior
   - incorrect test data
   - an incorrect assertion
   - an environment/setup problem
4. Inspect the relevant page state when possible.
5. Make the smallest justified correction.
6. Rerun the affected test.
7. Preserve the original failure as useful evidence when discussing limitations or Skill improvements.

Never hide a generated-code failure by silently changing unrelated test logic.

## Step 9 — Static review before execution

Before running generated code, perform a lightweight static review for common automation-quality problems:

- arbitrary sleeps
- absolute XPath or brittle positional selectors
- missing assertions
- hardcoded answers to dynamic requirements
- accidental real credentials or secrets
- selectors that were invented without evidence
- syntax/import problems visible from inspection

Static validation supplements browser execution; it does not replace it.

## Security and scope

Use only intended test environments. Do not perform real purchases, destructive account actions, credential harvesting, or access to private data. Never hardcode or expose real secrets supplied for unrelated systems.

Public demo credentials may be represented as constants when they are intentionally published for the test application, but real environment credentials should come from secure configuration or secret management.

## Output quality bar

The final automation should be:

- executable
- readable
- deterministic
- maintainable
- assertion-driven
- synchronized correctly
- based on stable, evidence-supported locators
- honest about uncertainty
- reproducible by another engineer

The goal is to encode the reasoning of a good SDET, not merely to translate English sentences into browser commands.
