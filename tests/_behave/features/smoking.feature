Feature: Smoke test

    Scenario: Smoke on the water
        Given I go to the homepage
         Then "volunteers" is in the page body
          And "help" is in the page body
