# Skill Examples

## Example A — Specific product

Input: "Add Sauce Labs Backpack to the cart."

Reasoning:
- Identify the product card by its exact product name.
- Scope the Add to cart action to that card.
- Avoid clicking the first Add to cart button on the page.
- Assert the cart contains the expected product.

## Example B — Dynamic product

Input: "Add the cheapest product to the cart."

Reasoning:
- Identify all product cards.
- Read displayed prices.
- Convert prices to numeric values.
- Find the minimum price and corresponding product.
- Click Add to cart inside that product card.
- Assert the selected product appears in the cart.

## Example C — Ambiguous instruction

Input: "Click the product."

Reasoning:
- Multiple products exist.
- No product identity is provided.
- Do not choose the first product arbitrarily.
- Ask for the product name or another disambiguating condition.
