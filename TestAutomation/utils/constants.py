# utils/constants.py

# --- Basis-Konfiguration (URLs und Timeouts) ---

BASE_URL = "https://grocerymate.masterschool.com"

# URLs für die Navigation
LOGIN_URL = f"{BASE_URL}/auth"
SHOP_URL = f"{BASE_URL}/store"
CHECKOUT_URL = f"{BASE_URL}/checkout"

# Standard-Timeout (für explizite Waits)
DEFAULT_WAIT_TIME = 10 # Sekunden

# Benutzerdaten
TEST_USER_EMAIL = "test@test32567.de"
TEST_USER_PASSWORD = "test123"
TEST_USER_NAME = "Testi Mc_tester" # Benutzername, der in Bewertungen angezeigt wird

# Produkt-Namen (für die ShopPage.find_product_card Logik)
PRODUCT_CHERRIES = "Cherries"
PRODUCT_APPLES = "Pink Lady Apples"
PRODUCT_ORANGES = "Oranges"
PRODUCT_PEARS = "Loose Pears"

# Produkt-URLs (für die Rating-Tests)
PRODUCT_ORANGES_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb4798f"
PRODUCT_PEARS_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb47990"
PRODUCT_CHERRIES_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb47991"

# Standard-Geburtsdatum für Altersfreigabe (älter als 18)
AGE_CONFIRMATION_DATE = "27-08-2007"

# Erwartete Fehlermeldung
RATING_REQUIRED_ERROR = "Invalid input for the field 'Rating'. Please check your input."