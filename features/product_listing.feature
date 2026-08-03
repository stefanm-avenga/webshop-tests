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
