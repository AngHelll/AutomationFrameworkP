Feature: Example Domain Page
  Simple example demonstrating BDD with Behave

  @smoke @example
  Scenario: Example.com loads successfully
    Given I navigate to "https://example.com/"
    Then the page title should contain "Example Domain"
    And the main header should be visible

  @example
  Scenario: Header text is correct
    Given I navigate to "https://example.com/"
    When I get the main header text
    Then it should contain "Example Domain"

  @example
  Scenario: Paragraph text is visible
    Given I navigate to "https://example.com/"
    Then the paragraph text should be displayed

  @example
  Scenario: More information link exists
    Given I navigate to "https://example.com/"
    Then a link should be present on the page

