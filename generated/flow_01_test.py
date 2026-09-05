import re

from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
PRODUCT_NAME = "Sauce Labs Backpack"


def test_flow_01_login_and_add_backpack(page: Page) -> None:
    """Flow 1: login, add Sauce Labs Backpack, and verify the cart."""

    # Step 1: Open the target application.
    page.goto(BASE_URL)

    # Step 2: Log in using the supplied demo credentials.
    page.locator("#user-name").fill(USERNAME)
    page.locator("#password").fill(PASSWORD)
    page.get_by_role("button", name="Login").click()

    # Step 3: Verify successful login by checking the Products heading.
    expect(page.get_by_text("Products", exact=True)).to_be_visible()
    expect(page).to_have_url(re.compile(r".*/inventory\.html$"))

    # Step 4: Identify the requested product and scope the action to its card.
    product_card = page.locator(".inventory_item").filter(has_text=PRODUCT_NAME)
    expect(product_card).to_have_count(1)
    expect(product_card.get_by_text(PRODUCT_NAME, exact=True)).to_be_visible()

    # Step 5: Add only the requested product to the cart.
    product_card.get_by_role("button", name="Add to cart").click()

    # Step 6: Open the shopping cart.
    page.locator('[data-test="shopping-cart-link"]').click()

    # Step 7: Verify the expected product is present.
    cart_item = page.locator(".cart_item").filter(has_text=PRODUCT_NAME)
    expect(cart_item).to_have_count(1)
    expect(cart_item.get_by_text(PRODUCT_NAME, exact=True)).to_be_visible()

    # Step 8: Verify exactly one cart item exists.
    expect(page.locator(".cart_item")).to_have_count(1)

    # Step 9: Verify the selected product is the expected product.
    expect(page.locator(".inventory_item_name")).to_have_text([PRODUCT_NAME])
