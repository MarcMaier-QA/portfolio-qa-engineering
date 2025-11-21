# Testplan – GroceryMate

## **1. Produktanalyse**

**Zielsetzung**
*Was ist das Ziel des Produkts?*
  - Das Ziel des Produkts GroceryMate ist es, Nutzern den Online-Einkauf von 
    Lebensmitteln und alkoholischen Getränken zu ermöglichen.
    Die Anwendung soll einen einfachen, 
    schnellen und benutzerfreundlichen Einkaufsvorgang bieten 
    von der Produktsuche über die Filterung bis hin zur Favoritenverwaltung.
  - Fokus liegt auf einer intuitiven Benutzeroberfläche und funktionierender Produktsuche.


**Zielnutzergruppe**
*Wer nutzt das Produkt? Wer sind die relevanten Stakeholder auf Nutzerseite?*
  - Die primäre Zielgruppe der Anwendung besteht aus technikaffinen Jugendlichen und jungen Erwachsenen
    im Alter von 15–25 Jahren, die hauptsächlich im Gaming-Bereich aktiv sind und Wert auf eine einfache,
    schnelle und bequeme Onlinebestellung von Lebensmitteln legen.

#### - **Typische Merkmale dieser Zielgruppe:**
- Digitale Routine:
  - Nutzen regelmäßig Smartphones, Discord, Twitch, Gaming-Plattformen; erwarten kurze Ladezeiten und klare Navigation.

- Verhaltensmuster beim Einkauf:
  - Bestellen Snacks, Getränke und schnelle Mahlzeiten häufig abends/nachts oder am Wochenende;
    erwarten intuitive Suchfunktionen und schnelle Wiederbestellung.

- Gesundheitsbewusstsein:
  - Trotz Gaming-Lifestyle achten viele auf energiereiche,
    teilweise gesunde Produkte (Protein-Snacks, Energydrinks, Meal-Prep-Zutaten).

- Spezielle Anforderungen:
  - Oft ungeduldig → niedrige Toleranz für UI-Fehler
  - Kaufen gelegentlich Produkte mit Altersbeschränkung (z. B. Energydrinks mit Alterscheck, alkoholische Getränke ab 18)
  - Legen Wert auf einfache Registrierung (Google/Discord Login, klare Fehlerhinweise)

- Relevante Stakeholder:
  - Privatkunden dieser Altersgruppe, Produktmanagement und das Entwicklungsteam.


**Hardware- und Software-Spezifikationen**
  - Die Anwendung soll auf gängigen Desktop- und Mobilgeräten funktionieren.
  - Getestet wird auf Standardkonfigurationen, die eine realistische Nutzung abbilden.


- **Hardwareanforderungen:**
    - Geräte: PCs, Laptops, Smartphones, Tablets
    - Spezifikationen:
      - Standardkonfigurationen für Android- und iOS-Geräte; Desktops mit mindestens 4 GB RAM und 2 GHz Prozessor


- **Softwareanforderungen:**
    - Betriebssysteme: Windows, macOS, Android, iOS
    - Browser: Chrome, Firefox, Safari, Edge


**Funktionalität des Produkts**
  - Registrierung und Login/Logout
  - Produktsuche über Suchleiste
  - Filterung und Sortierung von Produkten (z. B. nach Preis, Name, Empfehlung)
  - Favoritenfunktion (Produkte speichern, anzeigen, sortieren)
  - Navigationsmenü mit Seiten: Home, Shop, Favorites, Contact
  - Responsive Design für Desktop und Mobilgeräte

---

## **2. Teststrategie entwerfen**

**Testumfang (Scope of Testing)**

- **Im Umfang enthalten:**

    *Welche Funktionalitäten werden getestet?*
        - Testumfang (Scope of Testing)
        - Navigation: Überprüfung, ob die Hauptnavigationsbuttons (Home, Shop, Favorites, Contact) 
          korrekt auf die jeweiligen Seiten führen.
        - Produktsuche: Test der Suchfunktion, z.B. nach „apple“, um sicherzustellen,
          dass passende Produkte angezeigt werden.
        - Registrierung und Login: Validierung des Benutzerregistrierungs- und Loginprozesses.
        - Altersverifikation: Überprüfung, ob das Alter korrekt erkannt wird
          (z.B. bei Eingabe zu jung, korrekt oder unrealistisch wie 2030).
        - Favoritenfunktion: Testen von Hinzufügen und Entfernen von Produkten sowie der Sortierfunktionen
          (Preis, Name, Empfehlung).


- **Nicht im Umfang enthalten:**

    *Was ist vom Test ausgeschlossen?*
        - Kauf- / Checkout-Funktion: Transaktionen werden nicht getestet.
        - Zahlungs- und Backend-Prozesse: Payment-Gateways, Datenbankintegration, externe Dienste.
        - Nicht-funktionale Tests, wie Performance, Last, Security


**Geplante Testarten**
*Welche Testarten werden für die neuen Funktionen benötigt?*
    - Funktionstests
        - Überprüfung, ob die Hauptfunktionen des Webshops wie vorgesehen arbeiten.
        - Dazu gehören Navigation, Suche, Login/Registrierung, Altersverifikation und Favoritenfunktion.

**Risiken und Gegenmaßnahmen**

| Bereich                 | Risiko                                                                                | Gegenmaßnahme                                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Zielgruppe**          | Ungeduldige Nutzer brechen Prozesse wegen langer Ladezeiten ab                        | Ladezeit-Checks; Tests mit schlechter Verbindung; verständliche Warte-/Fehlermeldungen             |
| **Zielgruppe**          | Altersverifikation blockiert legitime Nutzer oder lässt Minderjährige durch           | Tests mit Randfällen, falschen Formaten und Zahlendrehern; validierte 18+-Logik; klare Fehlertexte |
| **Produkte & Suche**    | Suche liefert irrelevante Ergebnisse (z. B. Gaming-typische Suchbegriffe)             | Tests mit typischen Keywords, Schreibfehlern und Synonymen; Relevanzsortierung prüfen              |
| **Favoriten**           | Produkte werden falsch oder nicht gespeichert / nicht zwischen Geräten synchronisiert | Hinzufügen/Entfernen testen; Cross-Device-Tests; Persistenz nach Login/Logout prüfen               |
| **Login/Registrierung** | Doppelte Accounts, unklare Fehlertexte, Abbrüche im Prozess                           | Tests mit vergebenen E-Mails; Social-Login-Tests; Fehlermeldungen optimieren                       |
| **Mobile Nutzung**      | UI-Fehler auf Smartphones, besonders im Dark Mode                                     | Tests auf iOS/Android; verschiedene Displaygrößen; Dark-Mode-Check                                 |
| **Performance**         | Such- oder Filterperformance bricht bei hoher Nutzung ein                             | Stresstests der Such-API; Grenzwerte (lange Listen, viele Filter) testen                           |
| **Projektorganisation** | Entwicklungsverzögerungen                                                             | Zeitpuffer einplanen                                                                               |
| **Projektorganisation** | Fehlende oder falsche Testdaten                                                       | Erstellung realistischer Mock-Daten                                                                |
| **Projektorganisation** | Ressourcenengpässe im Testteam                                                        | Vertreter einplanen; Tests priorisieren                                                            |


**Testlogistik (Testverantwortlichkeiten)**

- **Testmanager** – Marc Maier
  - Verantwortlich für Planung, Durchführung und Dokumentation der funktionalen Tests.
- **Endanwender für UAT (User Acceptance Test)** – Marc Maier
  - Führt die Tests aus Sicht eines Endnutzers durch und dokumentiert die Ergebnisse.

---

## **3. Testziele definieren**

**Ziele**
- Funktionalität:
    - Sicherstellen, dass alle Hauptfunktionen
      (Navigation, Suche, Login/Registrierung, Altersverifikation, Favoritenfunktion)
      wie vorgesehen arbeiten.

- Benutzeroberfläche (GUI):
    - Überprüfung, ob alle Buttons und Links korrekt funktionieren und
      die Navigation übersichtlich gestaltet ist.

- Benutzbarkeit (Usability):
    - Bewertung, ob die Benutzerführung intuitiv ist und
      Fehlermeldungen verständlich sowie konsistent angezeigt werden.

**Erwartete Ergebnisse**
  - Alle Buttons (Home, Shop, Favorites, Contact) führen auf die korrekte Seite.
  - Die Suchfunktion liefert relevante Produkte passend zur Eingabe(z.B. "apple" → Apfelsorten).
  - Registrierung und Login funktionieren mit validen Daten und verhindern doppelte Accounts.
  - Altersverifikation blockiert zu junge Nutzer korrekt und erlaubt gültige Altersangaben.
  - Beim Hinzufügen zu Favoriten erscheint aktuell fälschlicherweise eine Fehlermeldung
    („Failed to add to favorites“), das Produkt wird aber dennoch korrekt gespeichert
    → dies wird als UI-Fehler (nicht-blockierend) dokumentiert.
  - Die Anwendung reagiert schnell und ohne merkbare Verzögerungen.

---

## **4. Testkriterien definieren**

**Aussetzungskriterien (Suspension Criteria)**

- **Blockierende Fehler in Kernfunktionen:**
  
  Treten kritische Fehler auf, die den Zugriff auf zentrale Funktionen wie Login, Navigation oder Produktsuche
  verhindern, wird der Testzyklus sofort ausgesetzt.

- **Nicht verfügbare Testumgebung:**

  Ist die Testumgebung nicht erreichbar oder fallen essenzielle Komponenten (z.b. Server, Datenbank) aus,
  werden Tests pausiert, bis die Umgebung stabil ist.

- **Abbruch bei unbrauchbaren Testdaten:**

  Sollten die zur Verfügung stehenden Testdaten fehlerhaft oder unvollständig sein,
  werden die Tests bis zur Bereitstellung gültiger Daten gestoppt.

- **Sonstige kritische Störungen:**

  Jegliche andere schwerwiegende Systemstörungen, die das Testergebnis verfälschen oder die Sicherheit
  der Testumgebung gefährden, führen zur temporären Unterbrechung.

- **Organisatorische Aussetzungen:**

  Tests werden ausgesetzt, wenn die Testdurchführung aufgrund betrieblicher Gegebenheiten wie Feiertagen,
  Betriebsferien oder geplanten Wartungsfenstern nicht möglich ist.

**Abnahmekriterien (Exit Criteria)**

- **Testdurchführung abgeschlossen:**
  - Alle geplanten funktionalen Tests (Navigation, Suche, Registrierung, Altersprüfung, Favoritenfunktion) wurden durchgeführt.

- **Ergebnisqualität:**

  - **Bestehensquote:** ≥ 80% der Testfälle erfolgreich bestanden.

  - Alle kritischen und hochpriorisierten Defekte wurden identifiziert und dokumentiert.

  - Bekannte mittlere oder geringe Fehler (z.B. UI-Fehler bei Favoritenfunktion) sind vermerkt,
    blockieren jedoch nicht die Freigabe.

- **Fehlerbehebung:**
  - Kritische Fehler (Severity 1 und 2) wurden behoben oder für die Abnahme priorisiert.

- **Testdokumentation:**
  - Testergebnisse, Defect Reports und UAT-Freigabedokumentation liegen vollständig vor.

- **Nicht-funktionale Aspekte:**
  - Performance- und Sicherheitsaspekte waren nicht Bestandteil dieses Testzyklus; bekannte Einschränkungen sind dokumentiert.

---

## **5. Ressourcenplanung**

- **Personelle Ressourcen:** 
  - QA Engineer: Marc Maier
  - Endanwender für UAT: Marc Maier
- **Hardware:**
  - MacBook(Desktop)
- **Software:**
  - Browser: Chrome
  - Betriebssystem: macOS
  - Tools: GitHub für Testdokumentation
- **Infrastruktur:**
  - Testumgebung: (https://grocerymate.masterschool.com/store/favs)
  - Automatisierungs-Tools: bisher keine, funktionale Tests manuell

---

## **6. Testumgebung planen**

- **Testgeräte:**
  - MacBook(Desktop)
  - Desktop-Browser: Chrome
- **Umgebungen:**
  - Entwicklung (DEV)
  - Test (TEST)
  - Abnahme (ACC – Acceptance)
  - Produktion (PROD)
- **Zusätzliche Hinweise:**
  - Testa manuel über Browser
  - Screenshots und Notizen Dienen der Dokumentation
  - Keine automatisierten Tools aktuell, nur manuelle Durchführung 

---

## **7. Zeitplan und Aufwandsschätzung**

|  Aktivität                                                                  | Startdatum | Enddatum   | Umgebung | Verantwortlich | Geplanter Aufwand |
|-----------------------------------------------------------------------------|------------|------------| -------- | -------------- | ----------------- |
| Testplanung                                                                 | 03.11.2025 | 03.11.2025 | Alle     | Marc Maier     | 3 Stunden         |
| Testfalldesign                                                              | 03.11.2025 | 03.11.2025 | Alle     | Marc Maier     | 5 Stunden         |
| Funktionale Tests (Navigation, Suche, Login, Altersverifikation, Favoriten) | 04.11.2025 | 04.11.2025 | TEST     | Marc Maier     | 6 Stunden         |
| Dokumentation der Testergebnisse                                            | 05.11.2025 | 05.11.2025 | TEST     | Marc Maier     | 2 Stunden         |
| Review und Abschlussbewertung                                               | 05.11.2025 | 05.11.2025 | TEST     | Marc Maier     | 2 Stunden         |
| Abnahmetest (UAT)                                                           | 05.11.2025 | 05.11.2025 | ACC      | Marc Maier     | 1 Stunde          |
**Gesamter Aufwand: ca. 19 Stunden**
(verteilt auf 3 Tage)

---

## **8. Testartefakte (Test-Deliverables)**

- Folgende Dokumente und Ergebnisse werden im Rahmen des Testprozesses für GroceryMate erstellt und bereitgestellt:
  - Testplandokument: Enthält Zielsetzung, Strategie, Umfang und Ablauf der Tests (dieses Dokument).
  - Testfälle und Testskripte: Detaillierte manuelle Testfälle für Navigation, Suche, Login/Registrierung,
    Altersverifikation und Favoritenfunktion.
  - Testdaten: Manuell erstellte Beispielnutzerdaten (z. B. verschiedene Geburtsdaten und Accounts) zur Überprüfung der
    Altersverifikation und Loginfunktion. 
  - Testberichte: Zusammenfassung der Testergebnisse, inklusive Anzahl bestandener/nicht bestandener Testfälle.
  - Fehlerberichte (Defect Reports): Dokumentation aufgetretener Fehler mit Beschreibung, Schweregrad und Status.
  - UAT-Freigabedokumentation (Sign-off): Bestätigung, dass die getesteten Funktionen den Anforderungen entsprechen und
    für die Abnahme freigegeben werden.
