# Test Execution - GroceryMate

**Tester:** Marc Maier  
**Datum:** 21.11.2025  
**Testumgebung:** Chrome 142 / MacOS 15.6.1 

---

## TC-01 Produkt bewerten (5 Sterne + Kommentar)

* **Precondition:** Eingeloggt, Produkt `Oranges` gekauft, Produktseite geöffnet
* **Steps:**
  1. Scrolle zum Bewertungsbereich.
  2. Wähle 5 Sterne aus.
  3. Trage Kommentar "Tolles Produkt!" ein.
  4. Klicke auf **Send**.
* **Expected Result:** Bewertung erscheint korrekt mit 5 Sternen, Kommentar und Username.
* **Actual Result:** 
* **Status:** 

---

## TC-02 Produkt bewerten (4 Sterne, kein Kommentar)

* **Precondition:** Eingeloggt, Produkt `Loose Pears` gekauft, Produktseite geöffnet
* **Steps:**
  1. Scrolle zum Bewertungsbereich.
  2. Wähle 4 Sterne aus.
  3. Lasse Kommentar-Feld leer.
  4. Klicke auf **Send**.
* **Expected Result:** Bewertung erscheint korrekt mit 4 Sternen, leerem Kommentar und Username.
* **Actual Result:** 
* **Status:** 

---

## TC-03 Bewertung ohne Sterne (nur Text)

* **Precondition:** Eingeloggt, Produkt `Cherries` gekauft, Produktseite geöffnet
* **Steps:**
  1. Scrolle zum Bewertungsbereich.
  2. Lasse Sterne ungewählt.
  3. Trage Kommentar "Gut" ein.
  4. Klicke auf **Send**.
* **Expected Result:** Popup erscheint oben mit Fehlermeldung, verschwindet automatisch, Bewertung wird nicht gespeichert.
* **Actual Result:** 
* **Status:** 

---

## TC-04 Altersverifikation: 18 Jahre (Zugriff erlauben)

* **Precondition:** Eingeloggt, Shop wird erstmals besucht
* **Steps:**
  1. Warte, bis Altersverifikations-Popup erscheint.
  2. Gib Geburtsdatum 27-08-2007 ein.
  3. Klicke auf **Bestätigen**.
* **Expected Result:** Zugriff auf alkoholische Produkte freigegeben, Popup mit Bestätigung erscheint und verschwindet automatisch.
* **Actual Result:** 
* **Status:** 

---

## TC-05 Altersverifikation: 17 Jahre (Zugriff verweigern)

* **Precondition:** Eingeloggt, Shop wird erstmals besucht
* **Steps:**
  1. Warte, bis Altersverifikations-Popup erscheint.
  2. Gib Geburtsdatum 27-08-2008 ein.
  3. Klicke auf **Bestätigen**.
* **Expected Result:** Zugriff auf alkoholische Produkte verweigert, Warn-Popup erscheint und verschwindet automatisch.
* **Actual Result:** 
* **Status:** 

---

## TC-06 Altersverifikation: Leeres Eingabefeld

* **Precondition:** Eingeloggt, Shop wird erstmals besucht
* **Steps:**
  1. Warte, bis Altersverifikations-Popup erscheint.
  2. Lasse Geburtsdatumsfeld leer.
  3. Klicke auf **Bestätigen**.
* **Expected Result:** Kein Zugriff auf alkoholische Produkte, Warn-Popup erscheint, Nutzer bleibt im Popup.
* **Actual Result:** 
* **Status:** 

---

## TC-07 Altersverifikation: Über 18 aber falsches Format

* **Precondition:** Eingeloggt, Shop wird erstmals besucht
* **Steps:**
  1. Warte, bis Altersverifikations-Popup erscheint.
  2. Gib Geburtsdatum 27.08.2007 ein.
  3. Klicke auf **Bestätigen**.
* **Expected Result:** Datum nicht erkannt, Nutzer wie unter 18 behandelt, Warn-Popup erscheint.
* **Actual Result:** 
* **Status:** 

---

## TC-08 Versandkosten: Bestellwert = 25 €

* **Precondition:** Eingeloggt, Warenkorb leer, Versandregel: 5 €, kostenlos ab 25 €
* **Steps:**
  1. Wähle 10x `Cherries` (2,50 € pro Stück)
  2. Klicke auf **Add to Cart**
  3. Öffne Warenkorb, prüfe Kostenbereich
* **Expected Result:** Versandkosten = 0 €, Total = 25 €
* **Actual Result:** 
* **Status:** 

---

## TC-09 Versandkosten: Bestellwert < 25 €

* **Precondition:** Eingeloggt, Warenkorb leer, Versandregel: 5 €, kostenlos ab 25 €
* **Steps:**
  1. Wähle 2x `Cherries` (2,50 € pro Stück)
  2. Klicke auf **Add to Cart**
  3. Öffne Warenkorb, prüfe Kostenbereich
* **Expected Result:** Versandkosten = 5 €, Total = 10 €
* **Actual Result:** 
* **Status:** 

---

## TC-10 Versandkosten: Änderung nach Entfernung von Produkten

* **Precondition:** Eingeloggt, Warenkorb leer, Versandregel: 5 €, kostenlos ab 25 €
* **Steps:**
  1. Wähle 9x `Cherries` + 1x `Pink Lady Apples` (25 €)
  2. Klicke auf **Add to Cart**
  3. Öffne Warenkorb → Versandkosten prüfen (0 €)
  4. Entferne `Pink Lady Apples` → Warenwert <25 €
  5. Versandkosten erneut prüfen
* **Expected Result:** Versandkosten wieder auf 5 € gesetzt
* **Observed Result / Bug:** Versandkosten bleiben 0 €
* **Actual Result:** 
* **Status:** 
