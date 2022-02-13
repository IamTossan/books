Feature: Page

Scenario: Create a page
    When I create a new page
    Then it is returned in the get route

Scenario: Create a page multiple times
    When I create a new page multiple times
    Then they are returned in the get route