Feature: Scraping Google Maps for Restaurants

Scenario: Scrape restaurants from Google Maps
    Given the user is on the Google Maps restaurants page
    When the user scrolls down and loads more restaurants
    Then the user should scrape and save information for 30 restaurants
    And the user should not have duplicate restaurant information