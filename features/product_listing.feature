Feature: Product listing
  As a shopper
  I want to browse the product catalogue
  So that I can find items to buy

  Scenario: All products are displayed by default
    Given the shop products page is open
    Then 8 product cards are displayed

  Scenario: Product cards show a name and a price
    Given the shop products page is open
    Then every product card shows a name and a price

  @ui @SHOP-4
  Scenario: Search by name filters the product grid
    Given the shop products page is open
    When the user searches for "mouse"
    Then only products containing "mouse" in their name are shown

  @ui @SHOP-4
  Scenario: Search and category filter combine with AND logic
    Given the shop products page is open
    When the user selects the "Electronics" category
    And the user searches for "mouse"
    Then only products in the "Electronics" category containing "mouse" in their name are shown

  @ui @SHOP-4
  Scenario: Search with no matches shows an empty product grid and a message
    Given the shop products page is open
    When the user searches for "zzznomatch"
    Then no product cards are displayed
    And the message "No products match your search." is shown

  @ui @SHOP-4
  Scenario: Clearing the search restores the full product list
    Given the shop products page is open
    When the user searches for "mouse"
    And the user clears the search
    Then 8 product cards are displayed

  @ui @SHOP-4
  Scenario: Search matching is case-insensitive
    Given the shop products page is open
    When the user searches for "MOUSE"
    Then only products containing "mouse" in their name are shown
