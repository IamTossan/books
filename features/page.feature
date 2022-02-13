Feature: Page

Scenario: Create a page
    When I create a new page
    Then it is returned in the get route
