
Feature: Fetch Company Details

  Scenario: Fetching Company Details
    Given He Opened Google Page
    When He Search Company Name "Actualize Consulting Engineers"
    When He Look For Card Apperance
    Then He Save Details Of Company

  Scenario Outline: Details Of Company
    Given He Opened Google Page
    When He Search Company Name "<company_name>"
    When He Look For Card Apperance
    Then He Save Details Of Company
    Examples:
      | company_name               |
      | Tech Mahindra              |
      | g7cr                       |
      | Fime India Private Limited |
      |TCS                         |



Scenario: Fetch company details and save to CSV
    Given the user is on the Google search page
    When the user searches for "actualize consulting engineers"
    Then the user extracts the company details
    And the user saves the company details to a CSV file

