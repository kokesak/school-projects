Feature: User account actions

    Scenario: Successfully create na account
        Given user is not logged in
        And web browser is at "Register Account" page
        When user fills out correctly all required informations
        And user marks the "Privacy Policy" checkbox
        Then user's account is succesfully created

    Scenario: Unsuccessfull creation of an account when not agreeing with "Privacy Policy"
        Given user is not logged in
        And web browser is at "Register Account" page
        When user fills out correctly all required informations
        And user leavs the "Privacy Policy" checkbox empty
        Then user's account is not created

    Scenario: Incorrect e-mail address change
        Given user is logged in
        And web browser is at "Edit your account information" page
        When user changes e-mail address to "foo@foo"
        Then warning message about not valid e-mail is showed

    Scenario: Log out
        Given user is logged in
        When user clicks "Logout" under "My Account" button
        Then user is successfully logged out

    Scenario: Log in
        Given user is not logged in
        And web browser is at "Login" page
        When user fills out correct login credentials
        Then user is successfully logged in

    Scenario: User's shopping cart does not change when re-logging
        Given user is logged in
        And user's shopping cart contains an "MacBook Air"
        When user logs out of his account
        And successfully logs in back to his account
        Then user's shopping cart contains an "MacBook Air"
