Feature: Shopping Cart

    Scenario: Add item to an empty cart
        Given web browser is at "Laptops & Notebooks" products page
        When user clicks on "ADD TO CART" button of "MacBook Air"
        Then "MacBook Air" is added to the shopping cart

    Scenario: Remove item from shopping cart
        Given user's shopping cart contains an "MacBook Air"
        And web browser is at "Shopping cart" page
        When user clicks red button representing removal
        Then "MacBook Air" is removed from cart

    Scenario: Change quantity of an item
        Given user's shopping cart contains an "MacBook Air"
        And web browser is at "Shopping cart" page
        When user change quantity number to "20" and clicks "Update"
        Then user's shopping cart contains "20" items of "MacBook Air"

