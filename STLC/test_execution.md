# Test Execution - GroceryMate

**Tester:** Marc Maier  
**Datum:** 21.11.2025  
**Testumgebung:** Chrome 142 / MacOS 15.6.1 

---

## TC-01 Produkt bewerten (5 Sterne + Kommentar)

* **Precondition:** Eingeloggt mit Email = `test@test32567.de`, Password = `test123`, Produkt `Oranges` gekauft.
* **Steps:**
  1. Produktseite von `Oranges` öffnen.
  2. Scrolle zum Bewertungsbereich.
  3. Wähle 5 Sterne aus.
  4. Trage Kommentar "Tolles Produkt!" ein.
  5. Klicke auf **Send**.
* **Expected Result:** Bewertung erscheint korrekt mit 5 Sternen und Kommentar.
* **Actual Result:** Bewertung erscheint mit 5 Sternen und Username aber ohne Kommentar.
* ![Eingegebener_kommentar.png](../docs/screenshots/Eingegebener_kommentar.png)
* ![Angezeigter_Kommentar.png](../docs/screenshots/Angezeigter_Kommentar.png)
* **Status:** <font color="red">FAILED</font>

---

## TC-02 Produkt bewerten (4 Sterne, kein Kommentar)

* **Precondition:** Eingeloggt mit Email = `test@test32567.de`, Password = `test123`, Produkt `Loose Pears` gekauft.
* **Steps:**
  1. Produktseite von `Loose Pears` öffnen.
  2. Scrolle zum Bewertungsbereich.
  3. Wähle 4 Sterne aus.
  4. Lasse Kommentar-Feld leer.
  5. Klicke auf **Send**.
* **Expected Result:** Bewertung erscheint korrekt mit 4 Sternen und ohne Kommentar.
* **Actual Result:** Wie erwartet werden 4 Sterne ohne kommentar korrekt angezeigt.
* ![vier_sterne_kein_Kommentar.png](../docs/screenshots/vier_sterne_kein_Kommentar.png)
* ![Anzeige_vier_sterne_kein_Kommentar.png](../docs/screenshots/Anzeige_vier_sterne_kein_Kommentar.png)
* **Status:** <font color="Green">PASSED</font>

---

## TC-03 Bewertung ohne Sterne (nur Text)

* **Precondition:** Eingeloggt mit Email = `test@test32567.de`, Password = `test123`, Produkt `Cherries` gekauft.
* **Steps:**
  1. Produktseite von `Cherries` öffnen.
  2. Scrolle zum Bewertungsbereich.
  3. Lasse Sterne ungewählt.
  4. Trage Kommentar `Gut` ein.
  5. Klicke auf **Send**.
* **Expected Result:** Popup erscheint oben mit Fehlermeldung, verschwindet automatisch, Bewertung wird nicht gespeichert.
* **Actual Result:** Wie erwartet erscheint ein Popup und gibt die Fehlermeldung:
    `Invalid input for the field 'Rating'. Please check your input.` aus.
* ![Null_sterne_text_gut.png](../docs/screenshots/Null_sterne_text_gut.png)
* ![Fehlermeldung_bei_null_sternen.png](../docs/screenshots/Fehlermeldung_bei_null_sternen.png)
* **Status:** <font color="Green">PASSED</font>

---

## TC-04 Altersverifikation: 18 Jahre (Zugriff erlauben)

* **Precondition:** Eingeloggt mit Email = `test@test32567.de`, Password = `test123`, Shop wird erstmals besucht
* **Steps:**
  1. Klicke auf Shop
  2. Warte, bis Altersverifikations-Popup erscheint.
  3. Gib Geburtsdatum `27-08-2007` ein.
  4. Klicke auf **Bestätigen**.
* **Expected Result:** Zugriff auf alkoholische Produkte freigegeben, Popup mit Bestätigung erscheint und verschwindet automatisch.
* **Actual Result:** Zugriff auf alkoholische Produkte freigeben, Popup mit Bestätigung erscheint und verschwindet automatisch.
* ![Age-Popup.png](../docs/screenshots/Age-Popup.png)
* ![Altersangabe_mit_27-08-2007.png](../docs/screenshots/Altersangabe_mit_27-08-2007.png)
* **Status:** <font color="Green">PASSED</font>

---

## TC-05 Altersverifikation: 17 Jahre (Zugriff verweigern)

* **Precondition:** Eingeloggt mit Email = `test@test32567.de`, Password = `test123`, Shop wird erstmals besucht
* **Steps:**
  1. Klicke auf **Shop**
  2. Warte, bis Altersverifikations-Popup erscheint.
  3. Gib Geburtsdatum `27-08-2008` ein.
  4. Klicke auf **Bestätigen**.
* **Expected Result:** Zugriff auf alkoholische Produkte verweigert, Warn-Popup erscheint und verschwindet automatisch.
* **Actual Result:** Zugriff auf alkoholische Produkte verweigert, Warn-/Hinweis-Popup erscheint und verschwindet automatisch.
* ![Altersangabe_mit_27-08-2008.png](../docs/screenshots/Altersangabe_mit_27-08-2008.png)
* ![Underage.png](../docs/screenshots/Underage.png)
* **Status:** <font color="Green">PASSED</font>

---

## TC-06 Altersverifikation: Leeres Eingabefeld

* **Precondition:** Eingeloggt mit Email = `test@test32567.de`, Password = `test123`, Shop wird erstmals besucht
* **Steps:**
  1. Klicke auf **Shop**
  2. Warte, bis Altersverifikations-Popup erscheint.
  3. Lasse Geburtsdatumsfeld leer.
  4. Klicke auf **Bestätigen**.
* **Expected Result:** Kein Zugriff auf alkoholische Produkte, Warn-Popup erscheint.
* **Actual Result:** Wie erwartet wird angenommen das der kunde unter 18 ist und bekommt den warn-Popup.
* ![Altersangabe_LEER.png](../docs/screenshots/Altersangabe_LEER.png)
* ![Underage.png](../docs/screenshots/Underage.png)
* **Status:** <font color="Green">PASSED</font>

---

## TC-07 Altersverifikation: Über 18 aber falsches Format

* **Precondition:** Eingeloggt mit Email = `test@test32567.de`, Password = `test123`, Shop wird erstmals besucht
* **Steps:**
  1. Klicke auf **Shop**
  2. Warte, bis Altersverifikations-Popup erscheint.
  3. Gib Geburtsdatum `27.08.2007` ein.
  4. Klicke auf **Bestätigen**.
* **Expected Result:** Datum nicht erkannt, Nutzer wie unter 18 behandelt, Warn-Popup erscheint.
* **Actual Result:** Datum nicht erkannt, Nutzer wird als unter 18 behandelt, Warn-Popup erscheint.
* ![Eingegebene_daten_bei_Altersabfrage.png](../docs/screenshots/Eingegebene_daten_bei_Altersabfrage.png)
* ![Underage.png](../docs/screenshots/Underage.png)
* **Status:** <font color="Green">PASSED</font>

---

## TC-08 Versandkosten: Bestellwert = 25 €

* **Precondition:** Eingeloggt mit Email = `test@test32567.de`, Password = `test123`, Warenkorb leer, Versandregel: 5 €, kostenlos ab 25 €
* **Steps:**
  1. Wähle 10x `Cherries` (2,50 € pro Stück)
  2. Klicke auf **Add to Cart**
  3. Öffne Warenkorb, prüfe Kostenbereich
* **Expected Result:** Versandkosten = 0 €, Total = 25 €
* **Actual Result:** Versandkosten werden korrekt mit 0 € angezeigt Total korrekt mit 25€.
* ![Zehn_Cherries_Versand_null_euro.png](../docs/screenshots/Zehn_Cherries_Versand_null_euro.png)
* **Status:** PASSED

---

## TC-09 Versandkosten: Bestellwert < 25 €

* **Precondition:** Eingeloggt mit Email = `test@test32567.de`, Password = `test123`, Warenkorb leer, Versandregel: 5 €, kostenlos ab 25 €
* **Steps:**
  1. Wähle 2x `Cherries` (2,50 € pro Stück)
  2. Klicke auf **Add to Cart**
  3. Öffne Warenkorb, prüfe Kostenbereich
* **Expected Result:** Versandkosten = 5 €, Total = 10 €
* **Actual Result:** Versandkosten korrekt bei 5 €, Total korrekt bei 10 € (5 € Versand + 5 € Wahrenwert).
* ![Zwei_Cherries.png](../docs/screenshots/Zwei_Cherries.png)
* **Status:** <font color="Green">PASSED</font>

---

## TC-10 Versandkosten: Änderung nach Entfernung von Produkten

* **Precondition:** Eingeloggt mit Email = `test@test32567.de`, Password = `test123`, Warenkorb leer, Versandregel: 5 €, kostenlos ab 25 €
* **Steps:**
  1. Wähle 7x `Cherries` + 1x `Pink Lady Apples` (20 €)
  2. Klicke auf **Add to Cart**
  3. Öffne Warenkorb → Versandkosten prüfen (0 €)
  4. Entferne `Pink Lady Apples` damit der Warenwert <20 € entspricht
  5. Versandkosten erneut prüfen
* **Expected Result:** Versandkosten wieder auf 5 € gesetzt
* **Observed Result / Bug:** Versandkosten bleiben 0 €
* **Actual Result:** Versand wird **NICHT** auf 5 € hoch gesetzt sondern bleibt bei 0 €.
* ![Versandkosten_vor_Entfernug_von_produkt.png](../docs/screenshots/Versandkosten_vor_Entfernug_von_produkt.png)
* ![Versandkosten_nach_Entfernung.png](../docs/screenshots/Versandkosten_nach_Entfernung.png)
* **Status:** <font color="red">FAILED</font>
