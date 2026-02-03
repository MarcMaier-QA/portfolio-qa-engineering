"""
Central configuration and test constants.

This module contains:
- URLs and navigation targets
- Test user credentials
- Product names and prices
- Shipping thresholds and expected totals
- Reusable values for UI and business logic tests

Keeping all constants in one place improves maintainability
and avoids hard-coded values across the test suite.
"""

# Base configuration (URLs & timeouts)
BASE_URL = "https://grocerymate.masterschool.com"

# Navigation URLs
LOGIN_URL = f"{BASE_URL}/auth"
SHOP_URL = f"{BASE_URL}/store"
CHECKOUT_URL = f"{BASE_URL}/checkout"

# Default timeout for explicit waits (in seconds)
DEFAULT_WAIT_TIME = 10

# Test user data
# Credentials for the dedicated test user
TEST_USER_EMAIL = "test@test32567.de"
TEST_USER_PASSWORD = "test123"

# Username as displayed in product reviews
TEST_USER_NAME = "testi Mc_tester"

# Product names (used for dynamic locators and shop navigation)
PRODUCT_CHERRIES = "Cherries"
PRODUCT_APPLES = "Pink Lady Apples"
PRODUCT_ORANGES = "Oranges"
PRODUCT_PEARS = "Loose Pears"

# Unit prices (used for subtotal and shipping calculations)
PRICE_CHERRY = 2.50
PRICE_PINK_LADY_APPLE = 2.50

# Expected subtotals for shipping-related test scenarios
TWO_CHERRIES_SUBTOTAL = 5.00
SEVEN_CHERRIES_SUBTOTAL = 17.50
TEN_CHERRIES_SUBTOTAL = 25.00

# Shipping costs and thresholds
SHIPPING_COST_STANDARD = 5.00
SHIPPING_COST_FREE = 0.00  # Applied when free-shipping threshold is reached

# Free shipping threshold (order value in €)
FREE_SHIPPING_THRESHOLD = 20.00

# Product URLs (used for direct navigation or rating-related tests)
PRODUCT_ORANGES_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb4798f"
PRODUCT_PEARS_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb47990"
PRODUCT_CHERRIES_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb47991"

# Alcohol products (age verification tests)
PRODUCT_IGNIS_VODKA_NAME = "Ignis French Grain Vodka"
PRODUCT_IGNIS_VODKA_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb47a8c"

# Default birthdate used to pass age verification (> 18 years)
AGE_CONFIRMATION_DATE = "27-08-2007"

# Expected validation and error messages
RATING_REQUIRED_ERROR = (
    "Invalid input for the field 'Rating'. Please check your input."
)
