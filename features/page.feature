Feature: Page

Scenario: Create a page
    Given the app is running
    When I create a new page
    Then it is returned in the get route

Scenario: Create a page multiple times
    Given the app is running
    When I create a new page multiple times
    Then they are returned in the get route

Scenario: Publish a page
    Given I created a page
    When I publish a page
    Then the page has a published state
