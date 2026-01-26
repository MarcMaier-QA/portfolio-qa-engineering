# Basis-Konfiguration (URLs und Timeouts)

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
TEST_USER_NAME = "testi Mc_tester" # Benutzername, der in Bewertungen angezeigt wird

# Produkt-Namen (für die ShopPage.find_product_card Logik)
PRODUCT_CHERRIES = "Cherries"
PRODUCT_APPLES = "Pink Lady Apples"
PRODUCT_ORANGES = "Oranges"
PRODUCT_PEARS = "Loose Pears"

# # Einheitspreise
PRICE_CHERRY = 2.50
PRICE_PINK_LADY_APPLE = 2.50

# Gesamtkosten der Produkte
TWO_CHERRIES_SUBTOTAL = 5.00
SEVEN_CHERRIES_SUBTOTAL = 17.50
TEN_CHERRIES_SUBTOTAL = 25.00

# Versandkosten
SHIPPING_COST_STANDARD = 5.00
SHIPPING_COST_FREE = 0.00    # ab 20€ Wahrenwert

# Versandkosten Schwellenwert
FREE_SHIPPING_THRESHOLD = 20.00 # Gratis Versand ab (20.00€)

# Produkt-URLs (für die Rating-Tests)
PRODUCT_ORANGES_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb4798f"
PRODUCT_PEARS_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb47990"
PRODUCT_CHERRIES_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb47991"

# Ignis French Grain Vodka
# Alkoholische Produkte (Shop / Altersprüfung)
PRODUCT_IGNIS_VODKA_NAME = "Ignis French Grain Vodka"
PRODUCT_IGNIS_VODKA_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb47a8c"

# Standard-Geburtsdatum für Altersfreigabe (älter als 18)
AGE_CONFIRMATION_DATE = "27-08-2007"

# Erwartete Fehlermeldung
RATING_REQUIRED_ERROR = "Invalid input for the field 'Rating'. Please check your input."