class InventoryLocators:
    TITLE = '[data-test="title"]'
    INVENTORY_ITEM = '[data-test="inventory-item"]'
    CART_LINK = '[data-test="shopping-cart-link"]'

    @staticmethod
    def add_to_cart_button(product_id: str) -> str:
        return f'[data-test="add-to-cart-{product_id}"]'

    @staticmethod
    def remove_from_cart_button(product_id: str) -> str:
        return f'[data-test="remove-{product_id}"]'
