# Test Cases for GroceryMate

## Konventionen

* **Precondition**: Zustand, der vor Ausführung des Tests vorhanden sein muss.
* **Steps**: nummerierte, reproduzierbare Schritte. Folge den Schritten genau.
* **Expected result**: Erwartetes Ergebnis bei korrekter Durchführung 
* **Automatisierbar?**: JA/NEIN

---

# Testfälle

### TC-01  Produkt bewerten (5 Sterne + Kommentar)

* **Precondition:**
  * Eingeloggt als gültiger Nutzer
  * Nutzer hat das Produkt `Oranges` zuvor gekauft
  * Produktseite von `Oranges` ist geöffnet*
* **Steps:**

  1. Scrolle zum Bewertungsbereich.
  2. Wähle 5 Sterne aus.
  3. Trage im Kommentar-Feld: `Tolles Produkt!` ein.
  4. Klicke auf **Send**.
* **Expected result:**

  * Die Bewertung wird erfolgreich gespeichert.
  * In der Bewertungsübersicht erscheint ein neuer Eintrag mit:
    * **Sternebewertung:** 5 von 5 Sternen(5 ausgefüllte Sterne werden angezeigt)
    * **Kommentar:** "Tolles Produkt!"
    * **Username:** Der korrekte Username des eingeloggten Nutzers wird angezeigt
* **Automatisierbar?:** JA

---

### TC-02 Produkt bewerten (4 Sterne, kein Kommentar)

* **Precondition:**
  * Eingeloggt als gültiger Nutzer
  * Nutzer hat das Produkt `Loose Pears` zuvor gekauft
  * Produktseite von `Loose Pears` ist geöffnet
* **Steps:**

  1. Scrolle zum Bewertungsbereich.
  2. Wähle 4 Sterne.
  3. Lasse das Kommentar-Feld leer.
  4. Klicke auf **Send**.
* **Expected result:**

   * Die Bewertung wird erfolgreich gespeichert.
   * In der Bewertungsübersicht erscheint ein neuer Eintrag mit:
     * **Sternebewertung:** 4 von 5 Sternen (4 ausgefüllte Sterne werden angezeigt)
     * **Kommentar:** Es wird kein Kommentar angezeigt, da das Feld leer blieb
     * **Username:** Der korrekte Username des eingeloggten Nutzers wird angezeigt
* **Automatisierbar?:** JA

---

### TC-03 Bewertung ohne Sterne (nur Text)

* **Automatisierbar?:** JA
* **Precondition:**
  * Eingeloggt als gültiger Nutzer
  * Nutzer hat das Produkt `Cherries` zuvor gekauft
  * Produktseite von `Cherries` ist geöffnet
* **Steps:**

  1. Scrolle zum Bewertungsbereich.
  2. Lasse die Sternebewertung ungewählt bzw wähle keine Sterne aus.
  3. Trage in das Kommentar-Feld `Gut` ein.
  4. Klicke auf **Send**.
* **Expected result:**

   * Ein Popup erscheint zentral oben auf der Seite mit der Fehlermeldung:
     `Invalid input for the field 'Rating'. Please check your input.`
   * Das Popup verschwindet nach kurzer Zeit automatisch.
   * Die Bewertung wird nicht gespeichert.
* **Automatisierbar?:** JA

---

### TC-04 Altersverifikation: 18 Jahre (Zugriff erlauben)

* **Precondition:** 
  * Nutzer ist als gültiger Benutzer eingeloggt.
  * Nutzer besucht den Shop zum ersten Mal nach dem Login.
  * Das Altersverifikations-Popup erscheint automatisch beim Betreten der Seite.
* **Steps:**

  1. Warte, bis das Popup zur Altersverifikation angezeigt wird.
  2. Gib als Geburtsdatum 27-08-2007 ein (entspricht exakt 18 Jahren)
  3. Klicke auf Bestätigen.
* **Expected result:**

  * Der Alterscheck wird erfolgreich bestanden.
  * Der Zugriff auf alkoholische Produkte wird freigeschaltet.
  * Ein Bestätigungs-Popup erscheint zentral unten mit der Meldung:
    `You are of age. You can now view all products, even alcohol products.`
  * Das Popup verschwindet automatisch nach kurzer Zeit.
* **Automatisierbar?:** JA

---

### TC-05 Altersverifikation: 17 Jahre (Zugriff verweigern)

* **Precondition:** 
  * Nutzer ist als gültiger Benutzer eingeloggt.
  * Nutzer besucht den Shop zum ersten Mal nach dem Login.
  * Das Altersverifikations-Popup erscheint automatisch beim Betreten der Seite.
* **Steps:**

  1. Warte, bis das Popup zur Altersverifikation angezeigt wird.
  2. Gib als Geburtsdatum 27-08-2008 ein (entspricht 17 Jahren und damit nicht volljährig).
  3. Klicke auf **Bestätigen**.
* **Expected result:**

  * Der Alterscheck schlägt fehl.
  * Alkoholische Produkte bleiben gesperrt.
  * Ein Warn-/Fehler-Popup erscheint zentral unten mit der Meldung:
    `You are underage. You can still browse the site, but you will not be able to view alcohol products.`
  * Das Popup verschwindet automatisch nach kurzer Zeit.
  * Der Nutzer sieht weiterhin nur nicht-alkoholische Produkte.
* **Automatisierbar?:** JA

---

### TC-06 Altersverifikation: Leeres Eingabefeld (keine Eingabe)

* **Precondition:** 
  * Nutzer ist als gültiger Benutzer eingeloggt.
  * Nutzer besucht den Shop zum ersten Mal nach dem Login.
  * Das Altersverifikations-Popup erscheint automatisch beim Betreten der Seite.
* **Steps:**

  1. Warte, bis das Popup zur Altersverifikation angezeigt wird.
  2. Lasse das Geburtsdatumsfeld komplett leer (keine Eingabe).
  3. Klicke auf **Bestätigen**.
* **Expected result:**

  * Das System führt keine Altersprüfung durch.
  * Der Nutzer bleibt im Popup, da keine Eingabe erfolgt ist.
  * Ein Warn-/Fehler-Popup erscheint zentral unten mit der Meldung:
    `You are underage. You can still browse the site, but you will not be able to view alcohol products.`
  * Alkoholische Produkte bleiben gesperrt.
  * Das Popup verschwindet automatisch nach kurzer Zeit.
  * Der Nutzer sieht weiterhin nur nicht-alkoholische Produkte.
* **Automatisierbar?:** JA

---

### TC-07 Altersverifikation: Über 18 aber falsches format

* **Precondition:** 
  * Nutzer ist als gültiger Benutzer eingeloggt.
  * Nutzer besucht den Shop zum ersten Mal nach dem Login.
  * Das Altersverifikations-Popup erscheint automatisch beim Betreten der Seite.
* **Steps:**

  1. Warte, bis das Popup zur Altersverifikation angezeigt wird.
  2. Gib als Geburtsdatum `27.08.2007` ein (benutzt Punkte statt `-`).
  3. Klicke auf Bestätigen.
* **Expected result:**

  * Das System erkennt das Eingabeformat nicht als gültiges Datum.
  * Es erfolgt keine echte Altersberechnung, daher wird der Nutzer wie „unter 18“ behandelt.
  * Ein Warn-/Fehler-Popup erscheint zentral unten mit der Meldung:
    `You are underage. You can still browse the site, but you will not be able to view alcohol products.`
  * Alkoholische Produkte bleiben gesperrt.
  * Das Popup verschwindet automatisch nach kurzer Zeit.
  * Nutzer sieht weiterhin nur nicht-alkoholische Produkte.
* **Automatisierbar?:** JA

---

### TC-08 Versandkosten: Versandkosten entfallen ab genau 25 € (Grenzwert)

* **Precondition:** 
  * Nutzer ist als gültiger Benutzer eingeloggt.
  * Der Warenkorb ist leer oder wurde gerade geleert.
  * Versandregel: 5 € Versandkosten, kostenlos ab 25 € Warenwert.
* **Steps:**

  1. Navigiere zum Shop
  2. Navigiere zu `Charries` und gib bei dem Feld, für die menge `10` ein
  3. klicke auf **Add to Cart**
  4. Öffne den Warenkorb
  5. Scrolle zum Kostenbereich, in dem die Versandkosten angezeigt werden.
* **Expected result:**

  * Die Versandkosten entfallen vollständig.
  * Die Anzeige im Warenkorb zeigt:
    * Shipment: 0 €
    * Product Total: 25 €
    * Total: 25 €
  * Der Nutzer kann mit kostenlosem Versand fortfahren.
* **Automatisierbar?:** JA

---

### TC-09 Versandkosten: Versandkosten bei Bestellwert unter 25 €

* **Precondition:** 
  * Nutzer ist als gültiger Benutzer eingeloggt.
  * Der Warenkorb ist leer oder wurde gerade geleert.
  * Versandregel: 5 € Versandkosten, kostenlos ab 25 € Warenwert.
* **Steps:**

  1. Navigiere zum Shop. 
  2. Wähle das Produkt Cherries aus und gib im Mengenfeld 2 Stück ein (Produktpreis 2,50 €, Warenwert 5 €).
  3. Klicke auf **Add to Cart**.
  4. Öffne den Warenkorb.
  5. Scrolle zum Kostenbereich, in dem die Versandkosten angezeigt werden.
* **Expected result:**

  * Versandkosten werden korrekt berechnet und angezeigt.
  * Die Anzeige im Warenkorb zeigt:
    * Shipment: 5 €
    * Product Total: 5 €
    * Total: 10 €
  * Der Nutzer kann mit der Zahlung fortfahren.
* **Automatisierbar?:** JA

---

### TC-10 Versandkosten: Änderung bei den Versandkosten

* **Precondition:**
  * Nutzer ist als gültiger Benutzer eingeloggt.
  * Der Warenkorb ist leer oder wurde gerade geleert.
  * Versandregel: 5 € Versandkosten, kostenlos ab 25 € Warenwert.
* **Steps:**

  1. Navigiere zum Shop.
  2. Wähle das Produkt `Cherries` aus und gib 9 Stück ein und 1-mal `Pink Lady Apples` (Warenwert 25 €, Versandkosten 0 €).
  3. Klicke auf Add to Cart.
  4. Öffne den Warenkorb und prüfe, dass Versandkosten 0 € angezeigt werden.
  5. Entferne `Pink Lady Apples`, sodass der Warenwert unter 25 € fällt.
  6. Scrolle zum Kostenbereich und prüfe die Versandkosten erneut.
* **Expected result:**

  * Versandkosten sollten wieder auf 5 € gesetzt werden, da der Warenwert jetzt <25 € beträgt.
  * Die Anzeige im Warenkorb zeigt korrekt:
    * Shipment: 5 €
    * Product Total: aktualisierter Warenwert
    * Total: Product Total + Shipment
  * Der Nutzer kann die Zahlung fortsetzen.
* Observed result / Bug:
  * Versandkosten bleiben auf 0 €, obwohl der Warenwert nun <25 € ist.
* **Automatisierbar?:** JA
