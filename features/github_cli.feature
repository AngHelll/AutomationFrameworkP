Feature: GitHub CLI Page
  As a developer
  I want to access GitHub CLI information
  So that I can download and use the CLI tool

  Background:
    Given I navigate to the GitHub CLI page

  @smoke @github
  Scenario: GitHub CLI page loads successfully
    Then the page should be loaded
    And the main header should be visible
    And the download button should be present

  @github @content
  Scenario: Main header contains expected text
    Then the main header should contain "Take GitHub to the command line"

  @github @downloads
  Scenario: Download button is available for Windows
    Then the Windows download button should be visible
    And the Windows download button should be clickable

  @github
  Scenario: Page navigation elements are present
    Then the navigation menu should be visible
    And the hero section should be present

  @github @refresh
  Scenario: Page refresh maintains content
    When I refresh the page
    Then the page should still be loaded
    And the main content should be visible

  @github @performance
  Scenario: Page loads within acceptable time
    When I measure the page load time
    Then the page should load in less than 30 seconds

