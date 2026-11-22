# Impressum und Datenschutzerklaerung (Entwuerfe)

Dieser Ordner wird nicht veroeffentlicht (`docs/` ist vom Pages-Deploy
ausgenommen). Die beiden Dateien sind **Entwuerfe mit Platzhaltern** und noch
nicht auf der Website verlinkt.

## Fertigstellen

1. In `Impressum.md` und `Datenschutz.md` alle Stellen in eckigen Klammern
   (`[...]`) durch die eigenen Angaben ersetzen. Kein Platzhalter darf bleiben:
   `grep -n '\[' docs/legal/*.md` muss danach leer sein.
2. Die Angaben zu den Diensten pruefen. Sie beschreiben den Stand vom
   22.11.2026 (GitHub Pages, Cloudflare vor `huskynarr.is-a.dev`,
   Cloudflare Web Analytics, Sentry-SDK mit eigenem Fehlerserver,
   Amazon-Partnerlinks, lokaler Browserspeicher). Aendert sich ein Dienst, muss
   der Text folgen.
3. Beide Dateien nach `web/impressum/README.md` und `web/datenschutz/README.md`
   verschieben oder als eigene Seiten anlegen und im Fuss von
   `web/index.html`, `web/configurator/`, `web/budget/` und `web/products/`
   verlinken. Danach `python3 tools/suit_sitemap.py` ausfuehren.

## Grenzen

Die Entwuerfe sind keine Rechtsberatung. Sie wurden aus dem technischen
Verhalten der Website abgeleitet, nicht von einer Anwaltskanzlei geprueft.
Vor der Veroeffentlichung selbst pruefen oder pruefen lassen.
