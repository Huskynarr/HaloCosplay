# Produktkatalog

Statische Katalogseite ohne Framework, Netzwerk-API, Tracking-Skript oder
Browser-Speicherung. Die Seite laesst sich zusammen mit dem Repository ueber
einen HTTP-Server oeffnen, etwa `python -m http.server 8000` und
`http://localhost:8000/web/products/`.

## Pflege

1. `Materials/ProductCatalog.json` bearbeiten: Produktkennung, Kategorie,
   Auswahlstatus, technische Grenzen, Mengenhinweis, zugeordnete Anleitungen
   und Ruestungsteile.
2. Herstellerquelle und konkreten Produktnamen abgleichen. `checked_on` nur
   setzen, wenn die Seite inhaltlich geprueft wurde; ein Datum ist kein
   Nachweis fuer Bestand, Preis oder Hardwarefreigabe.
3. Amazon-Suchlinks als `kind: search`, `affiliate: true` und mit der
   vorhandenen DE-Kennung fuehren. Keine ungeprueften ASINs uebernehmen.
4. `python tools/suit_catalog.py` ausfuehren. Dadurch entstehen `catalog.js`
   und `Materials/Einkaufsliste-Links.md` aus derselben Quelle.
5. `python tools/suit_catalog.py --check` und die Katalogtests ausfuehren.

Der vorhandene Amazon-Tag lautet `huskynarr-21`. Ob das Partnerkonto aktiv und
fuer Verguetungen berechtigt ist, wurde nicht geprueft. Die Seite verwendet
keine API-Zugangsdaten und liest keine Credentials. Herstellerlinks bleiben
ohne Partnerkennung; Affiliate-Links erhalten sichtbare Kennzeichnung und
`rel="sponsored nofollow noopener noreferrer"`.

## Verknuepfungen

- `?category=fog`: Baugruppe.
- `?guide=Documentation%2FGuides%2FMjolnir-Nebeltechnik.md`: Anleitung.
- `?part=helm`: Ruestungsteil im bestehenden 3D-Betrachter.
- `?product=fan`: einzelner Eintrag.
- `?q=RGB&source=direct`: Suchbegriff und Hersteller-/Datenblattquelle.

Filter lassen sich kombinieren und zuruecksetzen. Die bestehende
Anleitungsansicht fuegt passende Katalogeintraege automatisch hinzu; der
3D-Betrachter nutzt dieselbe Datenquelle. Das 3D-Modell selbst bleibt der
vorhandene Modellplatzhalter, solange kein eigenes Modell hinterlegt ist.

## Merkliste

Mengen sind ganze Zahlen von 1 bis 999. JSON speichert Produktkennungen und
Mengen mit `kind: halo_product_selection`. Ein Import verwendet ausschliesslich
Kennungen und Mengen; Texte, Links und Preise stammen wieder aus dem aktuellen
Katalog. Unbekannte oder doppelte Kennungen werden abgewiesen, die bisherige
Auswahl bleibt bei einem ungueltigen Import erhalten.

Preise sind unbekannt (`null`), nicht null Euro. CSV enthaelt leere Preisfelder.
Dieses Format wird bewusst nicht als Budgetplaner-Import ausgegeben: Dort
werden konkrete Planungswerte oder aktuelle Angebote manuell eingetragen.
Es erfolgt keine Bestellung, keine automatische Uebertragung an Shops und
keine automatische lokale Speicherung. Neuladen verwirft nicht exportierte
Auswahlen.

## Pruefung und Auslieferung

- Python validiert Quellen, Pfade, IDs und die erzeugten Ausgaben.
- JavaScript testet Filter, Affiliate-Erkennung, Export und Importgrenzen.
- Der Browsertest prueft echte Bedienung, Downloads, mobile Breite und
  Verknuepfungen mit dem Bauhandbuch.
- GitHub Pages veroeffentlicht weiterhin erst den Stand von `main` gemaess
  dem vorhandenen Deployment-Workflow. Ein Entwurfs-PR ist keine Live-Schaltung.
