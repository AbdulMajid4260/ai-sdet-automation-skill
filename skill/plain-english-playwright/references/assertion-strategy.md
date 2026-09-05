# Assertion Strategy Reference

Every meaningful test step should have an observable outcome where possible.

Examples:

- successful login → assert products heading is visible
- item added → assert cart badge/count or cart contents
- cart opened → assert cart page/heading
- expected product → assert exact product name
- expected number of items → assert locator count

Prefer Playwright web-first assertions because they retry while the page reaches the expected state.
