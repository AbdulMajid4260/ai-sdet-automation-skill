import re

from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"


def _price_from_card(card) -> float:
    """Read a displayed product price and convert it to a numeric value."""
    price_text = card.locator(".inventory_item_price").inner_text()
    return float(price_text.replace("$", "").strip())


def test_flow_02_dynamic_cheapest_product(page: Page) -> None:
    """Flow 2: identify the cheapest product dynamically and verify it in the cart."""

    page.goto(BASE_URL)
    page.locator("#user-name").fill(USERNAME)
    page.locator("#password").fill(PASSWORD)
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_text("Products", exact=True)).to_be_visible()

    # Sort through the user-facing sort control, but still compute the cheapest
    # product from the rendered data so the test does not depend on a hardcoded name.
    sort_control = page.locator(".product_sort_container")
    sort_control.select_option("lohi")

    products = page.locator(".inventory_item")
    expect(products.first).to_be_visible()

    product_count = products.count()
    prices = []
    for index in range(product_count):
        card = products.nth(index)
        prices.append((index, _price_from_card(card)))

    cheapest_index, cheapest_price = min(prices, key=lambda item: item[1])
    cheapest_card = products.nth(cheapest_index)
    cheapest_name = cheapest_card.locator(".inventory_item_name").inner_text()

    # Verify that the identified product really is the minimum displayed price.
    assert cheapest_price == min(price for _, price in prices)
    expect(cheapest_card.get_by_role("button", name="Add to cart")).to_be_visible()

    cheapest_card.get_by_role("button", name="Add to cart").click()
    page.locator('[data-test="shopping-cart-link"]').click()

    expect(page.locator(".cart_item")).to_have_count(1)
    expect(page.locator(".inventory_item_name")).to_have_text([cheapest_name])
