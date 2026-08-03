Feature: Product search filter
  As a shopper
  I want to search for products by name
  So that I can quickly find what I am looking for

  @ui @SHOP-5
  Scenario: Searching by name filters the product grid
    Given the shop products page is open
    When the user searches for "mouse"
    Then 1 product card is displayed
    And the product named "Wireless Mouse" is shown

  @ui @SHOP-5
  Scenario: Selecting a category limits which search results appear
    Given the shop products page is open
    When the user filters by the "Home" category
    And the user searches for "mouse"
    Then 0 product cards are displayed
    And the "No products match your search." message is shown

  @ui @SHOP-5
  Scenario: Search with no matching products shows the empty-state message
    Given the shop products page is open
    When the user searches for "zzz"
    Then 0 product cards are displayed
    And the "No products match your search." message is shown

  @ui @SHOP-5
  Scenario: Clearing the search restores the full product list
    Given the shop products page is open
    When the user searches for "mouse"
    And the user clears the search
    Then 8 product cards are displayed

  @ui @SHOP-5
  Scenario: Search is case-insensitive
    Given the shop products page is open
    When the user searches for "MOUSE"
    Then 1 product card is displayed
    And the product named "Wireless Mouse" is shown
