Feature: Gnereal functions of web

    Scenario Outline: Change currency
        Given web browser is at index page
        When user change currency to <currency>
        Then prices on website are changed to <currency>

        Examples:
            | currency |
            | EUR      |
            | GBP      |
            | USD      |

    Scenario: Price sorting low to high
        Given web browser is at "Laptops & Notebooks" products page
        And "Sort By:" box is set to "Default"
        When user changes "Sort By:" box to "Price (Low > High)"
        Then prices of items are sorted by price from low to high

    Scenario: Logging out resets the shopping cart
        Given user is logged in
        And user's shopping cart contains an "MacBook Air"
        When user clicks "Logout" under "My Account" button
        Then user shopping cart is empty
