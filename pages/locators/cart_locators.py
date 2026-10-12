class CartLocators:
    TITLE = '[data-test="title"]'
    CART_ITEM = '[data-test="inventory-item"]'
    CHECKOUT_BUTTON = '[data-test="checkout"]'
    CONTINUE_SHOPPING_BUTTON = '[data-test="continue-shopping"]'

    @staticmethod
    def remove_button(product_id: str) -> str:
        return f'[data-test="remove-{product_id}"]'
