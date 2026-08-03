Feature: Product search filter
  As a shopper
  I want to search for products by name
  So that I can quickly find what I am looking for

  @ui @SHOP-4
  Scenario: Search by name filters to matching products
    Given the shop products page is open
    When the user searches for "mouse"
    Then 1 product cards are displayed
    And the product named "Wireless Mouse" is shown

  @ui @SHOP-4
  Scenario: Search is case-insensitive
    Given the shop products page is open
    When the user searches for "MOUSE"
    Then 1 product cards are displayed
    And the product named "Wireless Mouse" is shown

  @ui @SHOP-4
  Scenario: Search and category filter combine to narrow results
    Given the shop products page is open
    When the user searches for "a"
    And the user selects the "Home" category
    Then 2 product cards are displayed

  @ui @SHOP-4
  Scenario: Search with no matches shows the empty-state message
    Given the shop products page is open
    When the user searches for "xyzzy"
    Then no product cards are displayed
    And the no-results message is shown

  @ui @SHOP-4
  Scenario: Clearing the search restores the full product list
    Given the shop products page is open
    When the user searches for "mouse"
    And the user clears the search
    Then 8 product cards are displayed

  # Supplementary: domain rule states substring match; a partial term must also match
  @ui @SHOP-4
  Scenario: Search matches on a partial name substring
    Given the shop products page is open
    When the user searches for "wire"
    Then 1 product cards are displayed
    And the product named "Wireless Mouse" is shown

  # Supplementary: verifies category-only filtering, which is a prerequisite for the combined-filter scenario
  @ui @SHOP-4
  Scenario: Category filter alone narrows the product list
    Given the shop products page is open
    When the user selects the "Stationery" category
    Then 2 product cards are displayed
