---
name: plain-english-playwright
# Keep this description specific so Claude can select the skill for web automation generation.
description: Convert plain-English web test steps and a target webpage into maintainable Python Playwright automation using explicit SDET reasoning for locators, synchronization, assertions, ambiguity, dynamic data, and validation.
---

# Plain-English Playwright Automation Skill

## Purpose

Convert a user's plain-English web test steps plus a target webpage/flow into working Python Playwright automation. The skill is not a click-translator: it applies explicit SDET reasoning before producing code.

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

If the application provides an explicit `data-test` or similar test contract, it may be preferable to a brittle CSS path. This is especially useful for icon-only controls whose accessible role has no reliable accessible name (for example, a shopping-cart link represented only by an icon/badge). Document the reason.

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

## Step 6 — Code generation

Generate complete executable Python using Playwright's synchronous API unless the user explicitly requests async.

Use pytest when the output is a test case.

Prefer a simple, readable test over a framework-heavy abstraction. Do not create page objects, factories, dependency injection, or utilities unless repeated behavior genuinely justifies them.

Use constants for stable test data such as the target URL and demo credentials. Do not commit real secrets.

## Step 7 — Validation mindset

Treat generated code as a candidate, not as proof of correctness.

Before presenting the final answer, review:

- Does every selector correspond to a plausible element?
- Is any selector unnecessarily brittle?
- Are dynamic states synchronized?
- Are assertions meaningful?
- Is the test deterministic?
- Are assumptions explicit?
- Are there arbitrary sleeps?
- Is any information hallucinated?
- Can another engineer reproduce the test?

If execution tools are available, run the test. If it fails, diagnose the root cause, correct the code, and rerun it. Never report a test as passing without execution evidence.

## Step 8 — Failure handling

When a locator or behavior cannot be verified:

1. Do not invent a selector.
2. Explain what is unknown.
3. Use available page/DOM/accessibility information if provided.
4. Ask for clarification only if the missing information blocks reliable generation.

## Security and scope

Use only intended test environments. Do not perform real purchases, destructive account actions, credential harvesting, or access to private data. Never hardcode or expose real secrets supplied for unrelated systems.

## Output quality bar

The final automation should be:

- executable
- readable
- deterministic
- maintainable
- assertion-driven
- synchronized correctly
- based on stable locators
- honest about uncertainty

The goal is to encode the reasoning of a good SDET, not merely to translate English sentences into browser commands.
