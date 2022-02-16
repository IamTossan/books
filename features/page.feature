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

Scenario: Update a page
    Given I created a page
    When I update the page
    Then the page is updated

Scenario: Update with a published page
    Given a page is published
    When I update the page
    Then a draft is created

Scenario: Comment a page
    Given a page is published
    When I make a comment on that page
    Then the comment is created
