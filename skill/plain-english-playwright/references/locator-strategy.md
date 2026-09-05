# Locator Strategy Reference

## Priority

1. Role + accessible name
2. Label
3. Placeholder
4. Test ID / explicit automation attribute
5. Stable ID
6. Stable CSS
7. Text for non-interactive content

## Repeated components

Scope the action to the component identified by the requested business text, then locate the control inside that component.

Example:

```python
product = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")
product.get_by_role("button", name="Add to cart").click()
```

The selector for the component should be verified against the target application. Prefer an explicit test contract if available.

## Avoid

- absolute XPath
- generated CSS classes
- coordinate clicks
- unnecessary positional selectors
- arbitrary `nth()` calls
- selectors based on presentation-only styling
