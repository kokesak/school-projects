Feature: Checkout functionality

    Background: user's shopping cart conatins an "MacBook Air"


    Scenario Outline: Begining of the checkout phase
        Given web browser is at index page
        And user is <state>
        When user clicks on "Checkout" button
        Then checkout phase is on step <step>

        Examples:
            | state         | step |
            | logged in     | 2    |
            | not logged in | 1    |

    Scenario: Successfull order - Logged in user
        Given user is logged in
        And web browser is at "Checkout" page on step: "Billing Details"
        When user continues correctly to make an order
        Then order is successfully created
