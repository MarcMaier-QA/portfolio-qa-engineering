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
  - Die Anwendung richtet sich an Endverbraucher verschiedener Altersgruppen,
    die online Lebensmittel und Getränke bestellen möchten.
  - Einschränkungen bestehen lediglich für Produkte mit Altersfreigabe (z. B. alkoholische Getränke, ab 18 Jahren).
  - Relevante Stakeholder auf Nutzerseite sind Privatkunden, das Produktmanagement und das Entwicklungsteam.


**Hardware- und Software-Spezifikationen**
  - Die Anwendung soll auf gängigen Desktop- und Mobilgeräten funktionieren.
  - Getestet wird auf Standardkonfigurationen, die eine realistische Nutzung abbilden.

- **Hardwareanforderungen:**
    - Geräte: PCs, Laptops, Smartphones, Tablets
    - Spezifikationen:
      - Standardkonfigurationen für Android- und iOS-Geräte; Desktops mit mindestens 4GB RAM und 2GHz Prozessor

- **Softwareanforderungen:**
    - Betriebssysteme: Windows, macOS, Android, iOS
    - Browser: Chrome, Firefox, Safari, Edge
    - Abhängigkeiten: Backend-Dienste, Zahlungsschnittstellen


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
        - Nicht-funktionale Tests, wie Performance, Last, Security (werden evtl. später durchgeführt). 


**Geplante Testarten**
*Welche Testarten werden für die neuen Funktionen benötigt?*
    - Funktionstests
        - Überprüfung, ob die Hauptfunktionen des Webshops wie vorgesehen arbeiten.
        - Dazu gehören Navigation, Suche, Login/Registrierung, Altersverifikation und Favoritenfunktion.

**Risiken und Gegenmaßnahmen**
| Bereich / Test          | Risiko                                                                  | Gegenmaßnahme                                                                                                         |
| ----------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Navigation**          | Klick auf einen Button führt auf falsche Seite oder falschen Inhalt     | Manuelles Durchklicken aller Hauptbuttons auf korrekte Seiten; Screenshots dokumentieren                              |
| **Produktsuche**        | Falsche Suchergebnisse (z.B. „apple“ → „egg“)                           | Test mit verschiedenen Suchbegriffen, Vergleich mit erwarteten Ergebnissen                                            |
| **Registrierung/Login** | Account wird doppelt erstellt, Passwort funktioniert nicht              | Test mit bestehenden und neuen Accounts; Überprüfung von Fehlermeldungen bei bereits registrierten Benutzern          |
| **Altersverifikation**  | Nutzer unter Mindestalter erhält Zugriff auf altersbeschränkte Produkte | Test mit verschiedenen Geburtstagen (zu jung, korrekt, unrealistisch) und Kontrolle, ob Zugang korrekt blockiert wird |
| **Favoritenfunktion**   | Produkte werden nicht oder falsch gespeichert                           | Test des Hinzufügens, Entfernens und Sortierens der Favoriten; Vergleich mit erwarteten Produkten                     |

- **Entwicklungsverzögerungen**
    → Gegenmaßnahme: Zeitpuffer im Zeitplan einplanen
    
- **Fehlende Testdaten**
    → Gegenmaßnahme: Erstellen von Testdaten (Mock-Daten)
    
- **Ressourcenengpässe**
    → Gegenmaßnahme: Ersatzpersonen identifizieren und einplanen
    

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
    -Bewertung, ob die Benutzerführung intuitiv ist und
     Fehlermeldungen verständlich sowie konsistent angezeigt werden.

**Erwartete Ergebnisse**
  - Alle Buttons (Home, Shop, Favorites, Contact) führen auf die korrekte Seite.
  - Die Suchfunktion liefert relevante Produkte passend zur Eingabe(z.b "apple" -> Apfelsorten).
  - Registrierung und Login funktionieren mit validen Daten und verhindern doppelte Accounts.
  - Altersverifikation blockiert zu junge Nutzer korrekt und erlaubt gültige Altersangaben.
  - Beim Hinzufügen zu Favoriten erscheint aktuell fälschlicherweise eine Fehlermeldung
    („Failed to add to favorites“), das Produkt wird aber dennoch korrekt gespeichert
    → dies wird als UI-Fehler (nicht-blockierend) dokumentiert.
  - Die Anwendung reagiert schnell und ohne merkbare Verzögerungen.

---

## **4. Testkriterien definieren**

**Aussetzungskriterien (Suspension Criteria)**
    - Kritische Fehler, die den Zugriff auf Hauptfunktionen
      (z. B. Login, Navigation, Suche) verhindern, blockieren die Fortsetzung der Tests.
    - Fests werden ausgesetzt, wenn die Testumgebung nicht erreichbar ist oder essentielle Komponenten
      (z. B. Server, Datenbank) ausfallen.

**Abnahmekriterien (Exit Criteria)**
    - Alle geplanten funktionalen Tests (Navigation, Suche, Registrierung, Altersprüfung, Favoriten) wurden ausgeführt.
    - **Ausführungsrate:** 100 % (5 / 5 Tests wurden durchgeführt)
    - **Bestehensquote:** 80 % (4 / 5 Tests erfolgreich, 1 Fehler beim Favoriten-Feature)
    - Alle kritischen und hochpriorisierten Defekte wurden identifiziert und dokumentiert.
    - Es bestehen keine offenen Fehler der Schweregrade 1 oder 2
    - Performanz- und Sicherheitsaspekte waren nicht Bestandteil dieses Testzyklus.
    - Sicherheitslücken wurden behoben
    - Der aktuelle Testzyklus kann mit dem Hinweis auf einen bekannten mittleren Defekt
      (Favoritenfunktion) abgeschlossen werden.

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