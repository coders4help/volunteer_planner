Feature: Landing Page

    Scenario: Get an overview
        Given I visit the home page
        Then I see the call to action "I want to help!" on the page
        And I see the call to action "Organize volunteers!" on the page
        And I see the section "What is it all about?"
        And I see the section "You can help at this locations:"
        And I see a button labeled "Login"
        And I see a button labeled "Start helping"
        And I see a navigation bar in the footer
