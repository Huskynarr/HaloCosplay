# Amazon Creators API - Link-Updater (lokal)

Aktualisiert die Amazon-Links in `Materials/Einkaufsliste-Links.md` und
`Materials/ShoppingList.md` ueber die **Amazon Creators API** (Nachfolger der
Product Advertising API, Login-with-Amazon OAuth 2.0).

## Warum lokal und nicht in GitHub Actions?

Die Seite ist eine **statische GitHub-Pages-Seite** - ein API-Secret kann dort
nicht sicher liegen (jeder koennte es aus dem Code lesen), und der
OAuth2-`client_credentials`-Flow funktioniert ohnehin nur serverseitig.
Deshalb der Ablauf:

1. Tool **lokal** ausfuehren -> schreibt die Markdown-Dateien neu (Preise,
   validierte ASINs).
2. Markdown **committen** -> der Deploy liefert die fertigen, einfachen Links.

Es landet also nie ein Secret im Repo.

## Setup

```bash
cp tools/amazon-creators/.env.example tools/amazon-creators/.env
# .env mit Credential ID + Secret fuellen (die .env ist gitignored)
```

Credentials: Amazon Associates Central -> Tools -> Creators API.
Region/Version: `3.2` = EU (deckt amazon.de ab).

## Nutzung

```bash
# 1) Parser pruefen, alle gefundenen Amazon-Links auflisten (KEIN API-Call)
node tools/amazon-creators/update-links.mjs --audit

# 2) Credentials + ein Beispiel-Produkt testen
node tools/amazon-creators/update-links.mjs --check

# 3) Preise aktualisieren / tote ASINs markieren (Account muss berechtigt sein)
node tools/amazon-creators/update-links.mjs --write

# 3b) zusaetzlich Such-Links in konkrete /dp/ASIN-Produktlinks aufloesen
node tools/amazon-creators/update-links.mjs --write --resolve-search
```

Keine Abhaengigkeiten - reines Node 18+ (globales `fetch`).

## Wichtig: Account-Berechtigung

Die Creators API liefert Produktdaten erst, wenn das Associate-Konto die
**Eignungskriterien** erfuellt (Creators API: ~10 qualifizierte Verkaeufe in
30 Tagen). Vorher antwortet die API mit:

```
403 AccessDeniedException - AssociateNotEligible
"Your account does not currently meet the eligibility requirements."
```

Der OAuth-Token wird trotzdem ausgestellt (Credentials gueltig) - nur die
Produktabfragen sind gesperrt. Sobald die Schwelle erreicht ist, funktioniert
`--write` ohne Aenderung.

## Sicherheit

- `.env` ist in `.gitignore` und darf **nie** committet werden.
- Wenn ein Secret doch einmal geteilt wurde: in der Amazon-Konsole **rotieren**.
