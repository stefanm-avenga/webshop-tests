Feature: Product search filter
  As a shopper
  I want to search and filter the product catalogue
  So that I can quickly find the products I am looking for

  @ui @SHOP-4
  Scenario: Searching by name shows only matching products
    Given the shop products page is open
    When the user searches for "mouse"
    Then only products whose name contains "mouse" are displayed

  @ui @SHOP-4
  Scenario: A search with no matches shows the empty-state message
    Given the shop products page is open
    When the user searches for "xyzzy"
    Then no product cards are displayed
    And the "No products match your search." message is shown

  @ui @SHOP-4
  Scenario: Search and category filter combine with AND semantics
    Given the shop products page is open
    When the user filters by category "Home"
    And the user searches for "mouse"
    Then no product cards are displayed

  @ui @SHOP-4
  Scenario: Clearing the search restores the full product list
    Given the shop products page is open
    When the user searches for "mouse"
    And the user clears the search
    Then 8 product cards are displayed

  @ui @SHOP-4
  Scenario: Search is case-insensitive
    Given the shop products page is open
    When the user searches for "MOUSE"
    Then only products whose name contains "mouse" are displayed
