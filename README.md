AI-Assisted SDET Automation Skill

1. Overview

This project demonstrates a Claude Skill that converts plain-English web test instructions into maintainable Python + Playwright automation while applying explicit Software Development Engineer in Test (SDET) reasoning.

The Skill is intentionally designed to be more than an English-to-code or English-to-click translator.

Before generating automation, it applies engineering rules for:

Natural-language interpretation

Locator selection and verification

Synchronization

Assertions

Dynamic data

Ambiguity handling

Failure diagnosis

Execution-based validation

The generated automation is treated as candidate code until it has been validated against the actual application.

2. Assignment Objective

The objective of this project is to demonstrate how an AI-assisted automation Skill can translate plain-English test scenarios into executable browser automation while still following good automation-engineering practices.

The demonstration uses SauceDemo:

https://www.saucedemo.com/

Two flows are used.

Flow 1 — Login and Add Specific Product

Plain-English requirement:

Open SauceDemo.

Log in using the standard demo credentials.

Verify that the Products page is displayed.

Find "Sauce Labs Backpack".

Add it to the cart.

Open the cart.

Verify that "Sauce Labs Backpack" is present.

Verify that exactly one product is present in the cart.

This flow demonstrates:

login automation

semantic/stable locator selection

product-component scoping

assertions

cart verification

synchronization

Flow 2 — Dynamically Find Cheapest Product

Plain-English requirement:

Open SauceDemo.

Log in using the standard demo credentials.

Verify that the Products page is displayed.

Sort products by Price, low to high.

Read the displayed products and prices.

Determine the cheapest product programmatically.

Add that product to the cart.

Open the cart.

Verify exactly one product is present.

Verify that the cart contains the dynamically identified cheapest product.

The product name is intentionally not hardcoded.

This flow demonstrates that the Skill can generalize beyond a fixed product scenario and reason about dynamic page data.

3. High-Level Architecture

Plain-English Test Steps + Target URL
                  |
                  v
        Claude Skill (SKILL.md)
                  |
                  v
          Interpret Test Intent
                  |
                  v
     Detect Assumptions / Ambiguity
                  |
                  v
          Locator Reasoning
                  |
                  v
   Synchronization + Assertion Design
                  |
                  v
       Dynamic-Data Reasoning
                  |
                  v
     Generate Python Playwright Test
                  |
                  v
          Static Validation
                  |
                  v
         Browser Execution
                  |
           +------+------+
           |             |
          PASS          FAIL
           |             |
           v             v
        Verified     Diagnose Cause
                         |
                         v
                Smallest Justified Fix
                         |
                         v
                       Rerun
                         |
                         v
                       PASS

The central design principle is:

AI-generated automation is a candidate until execution provides evidence that it works.

4. Technology Stack

Python

Playwright

pytest

pytest-playwright

Claude Skill

Chromium

SauceDemo

5. Why Playwright

Playwright was selected because it provides capabilities that are particularly useful for maintainable browser automation:

locator-based interactions

automatic actionability waiting

web-first assertions

role and accessibility-based locators

browser isolation

readable Python API

Chromium support

pytest integration

Playwright's auto-waiting also reduces the need for brittle fixed delays such as:

time.sleep(5)

or:

page.wait_for_timeout(5000)

The Skill explicitly discourages arbitrary sleeps as a normal synchronization strategy.

6. Why Python

Python was selected because it provides concise and readable automation code and makes the generated tests easy to explain during an SDET walkthrough.

It also makes dynamic-data operations, such as calculating the cheapest displayed product, straightforward.

7. Why pytest

pytest provides:

simple test discovery

readable assertions

Playwright fixture integration

concise execution commands

clear pass/fail reporting

The pytest-playwright plugin provides the Playwright page fixture used by the generated tests.

8. Why SauceDemo

SauceDemo was selected because it is a public application designed for automation/testing practice.

It provides useful testable behavior including:

authentication

product listings

product sorting

dynamic product selection

add-to-cart behavior

cart verification

It allows the project to demonstrate realistic browser automation without performing purchases or interacting with private production data.

9. Claude Skill Design

The Skill is located at:

skill/plain-english-playwright/SKILL.md

The Skill accepts:

A target URL or clearly identified web flow

Ordered plain-English test steps

Optional credentials/test data

Optional DOM/accessibility information

Optional framework constraints

The Skill produces, in order:

Test interpretation

Assumptions and ambiguities

Locator decisions

Synchronization decisions

Complete executable Playwright test

Validation checklist

Limitations or items requiring human verification

This structure forces the AI to expose important engineering decisions instead of only returning code.

10. Natural-Language Interpretation

The Skill classifies instructions into categories such as:

navigation

data entry

click/action

selection

extraction

assertion/verification

dynamic-data operation

conditional behavior

Actions and expected outcomes are separated.

For example:

Add the cheapest product to the cart

contains both a dynamic-data requirement and an action.

The Skill must first determine what "cheapest" means from rendered data before performing the Add-to-cart action.

11. Locator Strategy

The Skill uses the following preferred locator hierarchy:

get_by_role() with an accessible name

get_by_label()

get_by_placeholder()

get_by_test_id() where data-testid exists

Stable IDs or dedicated test attributes

Stable meaningful CSS selectors

Text locators when appropriate

The Skill avoids:

absolute XPath

deep DOM traversal

generated class names

unnecessary nth-child

coordinate clicks

arbitrary positional assumptions

invented selectors

For repeated components, actions are scoped to the component containing the requested business identity.

Example:

product = page.locator(".inventory_item").filter(
    has_text="Sauce Labs Backpack"
)

product.get_by_role(
    "button",
    name="Add to cart"
).click()

This is safer than selecting an arbitrary Add-to-cart button by position.

12. Locator Verification Gate

A major design improvement made during this assignment was adding an explicit locator-verification gate.

The Skill must not assume that a selector exists merely because:

it follows a common convention

it appears in documentation/examples

it existed in an older application version

it looks technically reasonable

The Skill distinguishes between:

Verified locator

Supported by actual DOM, accessibility, page inspection, or successful execution evidence.

Inferred locator

Reasonable based on available information but not directly verified against the current application.

Failed locator

Disproven through inspection or browser execution.

An inferred locator must never be presented as verified.

This distinction became important during real execution of the generated automation.

13. Synchronization Strategy

The Skill primarily uses Playwright's:

locator auto-waiting

actionability checks

web-first assertions

state-based synchronization

For example:

expect(
    page.get_by_text("Products", exact=True)
).to_be_visible()

is preferred over:

time.sleep(5)

The goal is to wait for a meaningful application state rather than an arbitrary amount of time.

14. Assertion Strategy

The generated automation verifies outcomes rather than merely executing actions.

Assertions are used for:

successful navigation

Products-page visibility

URL state

expected product visibility

cart badge state

expected cart contents

expected item count

dynamic-data results

For example:

expect(cart_items).to_have_count(1)

verifies a business outcome rather than merely confirming that the cart button was clicked.

15. Dynamic-Data Handling

Flow 2 intentionally tests dynamic reasoning.

The automation does not contain a hardcoded cheapest-product name.

Instead, it:

Reads product cards from the page

Extracts each product name

Extracts each displayed price

Converts price text into numeric values

Determines the minimum

Associates that minimum with the corresponding product

Adds that product to the cart

Verifies the same product in the cart

Conceptually:

Rendered products
       |
       v
Extract name + price
       |
       v
Convert prices to numbers
       |
       v
Calculate minimum
       |
       v
Identify corresponding product
       |
       v
Add that product
       |
       v
Verify cart

This demonstrates generalization rather than memorization of SauceDemo's current cheapest product.

16. Ambiguity Handling

Natural-language instructions are not always precise.

For example:

Click the product.

may be ambiguous if several products are displayed.

The Skill is instructed not to silently choose an arbitrary element.

If the surrounding context identifies one clear element, the Skill may state the assumption and continue.

If multiple valid interpretations remain, it should request clarification.

This prevents natural-language ambiguity from silently becoming nondeterministic automation.

17. AI-Assisted Validation Strategy

Generated automation is not automatically assumed to be correct.

The validation process is:

Generate
   |
   v
Review
   |
   v
Execute
   |
   +-------- PASS --------> Verified
   |
   FAIL
   |
   v
Inspect exact failure
   |
   v
Classify root cause
   |
   v
Correct smallest assumption
   |
   v
Rerun

Potential failure categories include:

incorrect locator

synchronization issue

incorrect assumption

incorrect test data

incorrect assertion

environment/setup problem

The Skill explicitly states:

Never report a test as passing without execution evidence.

18. Challenges and Lessons Learned

18.1 AI-Generated Locators Can Look Correct but Still Fail

One of the most important findings during this assignment was that an AI-generated selector can look technically valid while not matching the current application's DOM.

During validation, a cart-item locator based on an inferred data-test attribute did not resolve against the live SauceDemo page.

The failure was diagnosed as a locator mismatch rather than being treated as an unrelated automation problem.

The affected locator was corrected based on the actual application structure, and the test was rerun successfully.

This directly influenced the Skill's locator-verification rules.

18.2 Sort-Control Locator Failure

Another execution failure occurred in Flow 2.

The original locator was:

page.get_by_role("combobox", name="Sort by")

During browser execution, Playwright timed out while waiting for this locator.

The failure showed that a semantically attractive locator is not automatically a valid locator for the current page.

After validating the application, the locator was changed to:

page.locator(".product_sort_container")

The test was then rerun successfully.

This demonstrates an important SDET principle:

Locator quality depends on both stability and evidence that the locator actually resolves to the intended element.

18.3 Generalization

A second challenge was proving that the Skill was not simply reproducing a known SauceDemo scenario.

Flow 2 therefore introduces a dynamic requirement:

Find the cheapest product.

The automation computes the answer from rendered page data instead of hardcoding a known product.

This demonstrates that the Skill can convert higher-level test intent into automation logic.

18.4 AI Output Is Candidate Code

The project deliberately does not assume that AI-generated code is production-ready.

A generated test may contain:

an incorrect locator

an incorrect assumption

a synchronization problem

an invalid assertion

environment-specific behavior

Therefore, the final workflow requires execution and diagnosis.

The failures encountered during development were useful because they led to stronger Skill rules rather than being hidden.

19. Final Local Validation

Both baseline demonstration flows were executed locally against the live SauceDemo application using Chromium.

Final verified status:

Flow 1: PASS
Flow 2: PASS

Flow 1 and Flow 2 were rerun after correcting identified locator problems.

Execution duration is intentionally not treated as part of the expected result because it varies depending on machine and network conditions.

20. Project Structure

ai_sdet_automation_skill/
│
├── README.md
├── requirements.txt
├── pytest.ini
├── .gitignore
│
├── skill/
│   └── plain-english-playwright/
│       ├── SKILL.md
│       └── references/
│           ├── locator-strategy.md
│           ├── assertion-strategy.md
│           └── examples.md
│
├── tests/
│   ├── flow_01_login_and_cart.md
│   └── flow_02_sort_and_cart.md
│
├── generated/
│   ├── flow_01_test.py
│   └── flow_02_test.py
│
└── scripts/
    └── validate_generated_test.py

21. Environment Setup

Windows Command Prompt

Create the virtual environment:

python -m venv .venv

Activate it:

.venv\Scripts\activate

Install dependencies:

python -m pip install -r requirements.txt

Install Chromium for Playwright:

python -m playwright install chromium

After activation, the terminal should show something similar to:

(.venv) C:\path\to\ai_sdet_automation_skill>

22. PowerShell Setup

For PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium

If PowerShell execution policy prevents activation, commands can be run directly through the virtual environment:

.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium

23. Static Validation

From the project root:

python scripts\validate_generated_test.py generated\flow_01_test.py

and:

python scripts\validate_generated_test.py generated\flow_02_test.py

The static validator provides an additional check before browser execution.

Static validation does not replace real browser execution.

24. Running Flow 1

pytest generated\flow_01_test.py -v

Expected result:

PASSED

25. Running Flow 2

pytest generated\flow_02_test.py -v

Expected result:

PASSED

26. Running the Complete Test Suite

Run:

pytest generated\ -v

The expected final result is:

generated\flow_01_test.py ... PASSED
generated\flow_02_test.py ... PASSED

2 passed

27. Running With a Visible Browser

For the interview walkthrough, the browser can be shown using:

pytest --headed generated\flow_01_test.py -v

Flow 2 can be demonstrated using:

pytest --headed generated\flow_02_test.py -v

This allows the panel to see the generated automation interacting with the application.

28. Key Technical Decisions

Framework

Playwright was selected for locator-based automation, auto-waiting, browser support, and web-first assertions.

Language

Python was selected for readability and concise automation logic.

Test Runner

pytest was selected for straightforward test organization and Playwright fixture integration.

Application

SauceDemo provides a safe and deterministic public automation target.

Architecture

A focused Claude Skill plus small generated tests was preferred over building a large Page Object Model or enterprise automation framework.

The purpose of the assignment is to demonstrate AI-assisted test-generation reasoning rather than framework complexity.

Validation

Generated code is treated as candidate code and must be validated through execution whenever possible.

29. Assumptions

The project assumes:

SauceDemo remains publicly reachable.

The demo credentials remain valid.

Chromium can be installed and executed on the target machine.

The relevant SauceDemo UI structure remains compatible with the final validated locators.

Network connectivity is available during live browser execution.

30. Limitations

A Claude Skill cannot guarantee correct automation for every website.

Natural-language instructions may contain ambiguity requiring clarification.

Locator quality depends on the target application's DOM and accessibility/test contracts.

Website updates can invalidate previously working locators.

Static validation cannot replace browser execution.

Claude's execution environment may not always have browser or network access, so generated tests may require execution and DOM validation on the engineer's local machine.

Dynamic applications may require additional synchronization strategies.

The project does not include CI/CD infrastructure, Docker, advanced reporting, parallel execution, or a full production Page Object Model because those are outside the core assignment objective.

These would be reasonable extensions for a production automation framework.

31. Security and Scope

The Skill is designed for intended test environments.

It should not:

perform real purchases

perform destructive account operations

collect private credentials

access unrelated private information

expose production secrets

Only public demo credentials are used in this project.

32. Potential Future Improvements

If this proof of concept were extended into a production automation system, possible improvements would include:

Page Object Model where reuse justifies it

environment-based configuration

environment variables or secret management

CI/CD integration

HTML/Allure reporting

screenshots and traces on failure

multi-browser execution

parallel execution

test-data management

stronger DOM inspection before code generation

automated generated-test linting

retry policies for infrastructure-level failures

generation history and auditability

These were intentionally kept outside the current implementation to keep the assignment focused.

33. Live Walkthrough Plan

Recommended demonstration order:

Explain the problem:
"The Skill converts plain-English test steps into browser automation while enforcing SDET engineering rules."

Show the project structure.

Open SKILL.md.

Explain:

natural-language interpretation

locator hierarchy

locator verification

synchronization

assertions

ambiguity handling

dynamic-data handling

validation

Show the Flow 1 plain-English requirement.

Show the generated Flow 1 automation.

Run:

pytest --headed generated\flow_01_test.py -v

Explain why the product locator is scoped to the requested product.

Show Flow 2.

Explain why the cheapest product is determined dynamically rather than hardcoded.

Run:

pytest --headed generated\flow_02_test.py -v

Explain the locator failures encountered during development and how execution evidence improved the Skill.

Discuss limitations and future improvements.

34. Interview Explanation

A concise explanation of the solution is:

I designed the Claude Skill as a constrained automation-generation process rather than a simple prompt that translates English into clicks. The input consists of a target web flow and plain-English test steps. The Skill first interprets the intent and then applies explicit rules for locator selection, synchronization, assertions, ambiguity, dynamic data, and validation. It generates Python Playwright automation, but that output is treated as candidate code until it is validated. During development I encountered locators that looked reasonable but failed against the live DOM. Instead of hiding those failures, I used them to strengthen the Skill with a locator-verification gate and a failure-diagnosis process. Flow 1 demonstrates the basic automation path, while Flow 2 demonstrates generalization by dynamically determining the cheapest product instead of hardcoding its name.

35. Key Takeaway

The main lesson from this project is that AI can accelerate test-automation generation, but good automation still requires engineering judgment.

The Skill therefore combines:

AI generation
     +
SDET reasoning
     +
DOM/locator validation
     +
real browser execution
     +
failure diagnosis

The objective is not simply to generate code.

The objective is to generate automation that is understandable, maintainable, testable, and honest about uncertainty.