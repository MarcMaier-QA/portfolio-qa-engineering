## Hausaufgabe - XPath

### Beispiel HTML
````HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nested Complex HTML Document</title>
</head>
<body>
    <header>
        <h1 id="mainTitle">Welcome to Our Company</h1>
        <nav>
            <ul>
                <li><a href="#home" class="nav-link">Home</a></li>
                <li><a href="#about" class="nav-link">About Us</a></li>
                <li>
                    <a href="#services" class="nav-link">Services</a>
                    <ul class="dropdown">
                        <li><a href="#webdev">Web Development</a></li>
                        <li><a href="#graphicdesign">Graphic Design</a></li>
                        <li><a href="#seo">SEO Services</a></li>
                    </ul>
                </li>
                <li><a href="#contact" class="nav-link">Contact</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <section id="about">
            <h2 class="sectionTitle">About Us</h2>
            <div class="content">
                <p>We are a leading company in the industry.</p>
                <div class="team">
                    <h3>Our Team</h3>
                    <ul>
                        <li>
                            <h4>John Doe</h4>
                            <p>CEO</p>
                        </li>
                        <li>
                            <h4>Jane Smith</h4>
                            <p>CTO</p>
                        </li>
                    </ul>
                </div>
            </div>
        </section>
        <section id="services">
            <h2 class="sectionTitle">Our Services</h2>
            <div class="service-list">
                <div class="service-item">
                    <h3>Web Development</h3>
                    <p>Creating stunning websites.</p>
                </div>
                <div class="service-item">
                    <h3>Graphic Design</h3>
                    <p>Designing visual content.</p>
                </div>
                <div class="service-item">
                    <h3>SEO Services</h3>
                    <p>Improving search engine rankings.</p>
                </div>
            </div>
        </section>
        <section id="contact">
            <h2 class="sectionTitle">Contact Us</h2>
            <form id="contactForm">
                <label for="name">Name:</label>
                <input type="text" id="name" required>
                <label for="email">Email:</label>
                <input type="email" id="email" required>
                <label for="message">Message:</label>
                <textarea id="message" placeholder="Your Message"></textarea>
                <input type="submit" value="Send Message">
            </form>
        </section>
    </main>
    <footer>
        <p>&copy; 2023 Company Name. All rights reserved.</p>
    </footer>
</body>
</html>
````

---
## Grundidee der Slashes

// → bedeutet „suche irgendwo ab hier, rekursiv, nach diesem Element“.

/ → bedeutet „direkter Kindknoten“.

**Beispiele:**

```
//div          # alle <div> auf der gesamten Seite
/div           # nur das direkte Kind des aktuellen Kontexts
```

---

* **Haupt-`h1`Element finden:**
```
//h1[@id="mainTitle"]
```

---

* **Navigationslink `About Us` auszuwählen:**
```
//nav//a[@href='#about']
```

---

* **Dropdown-Link `Graphic Design`:**
```
//ul[@class='dropdown']//a[text()='Graphic Design']
```

---

* **Teammitgliedsname `Jane Smith`:**
```
//div[@class='team']//h4[text()='Jane Smith']
```

---

* **Beschreibung der `SEO Services` auswählen**
```
//div[@class='service-item'][h3/text()='SEO Services']/p
```

----

* **Alle Service-Elemente im Abschnitt `Our Services` auszuwählen:**
```
//section[@id='services']//div[@class='service-item']
```

----

* **`E-Mail`-Eingabefeld im Kontaktformular auszuwählen:**
```
//form[@id='contactForm']//input[@id='email']
```

----

* **`Gesamtes Kontaktformular` auszuwählen:**
```
//form[@id='contactForm']
```

---

* **`Footer-Absatz-Element` auszuwählen:**
```
//footer//p
```

----

* **Namen `<h4>` des ersten Teammitglieds:**
```
//div[@class='team']//ul/li[1]/h4
```

----

* **Beschreibung des zweiten `Service-Elements` auswählen:**
```
//section[@id='services']//div[@class='service-item'][2]/p
```

----

* **Überschrift der Sektion `'Contact Us'` `<h2> Element` auszuwählen:**
```
//section[@id='contact']/h2
```

---

* **Alle Links innerhalb des Dropdowns unter dem Navigationspunkt `"Services"` auszuwählen:**
```
//nav//li[a[text()='Services']]//ul[@class='dropdown']//a
```

----

* **das erste `<li>` im Abschnitt `Our Team` auszuwählen:**
```
//div[@class='team']//ul/li[1]
```

----

* **Schaltfläche `"Send Message"` im Kontaktformular zu finden:**
```
//form[@id='contactForm']//input[@type='submit' and @value='Send Message']
```
