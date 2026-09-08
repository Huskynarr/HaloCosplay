# Profilkonfigurator

Der lokale Konfigurator erfasst beliebig benannte Koerperprofile und eine
Baukonfiguration. Es gibt keine voreingestellte reale Person, Koerpergroesse oder
Schuhgroesse. Ruestungsreferenz, Materialweg, Betriebsart und optionale Ausstattung
sind unabhaengig waehlbar.

## Start

Im Repository-Stamm:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Danach `http://127.0.0.1:8000/web/configurator/` oeffnen. Auf GitHub Pages lautet
der Pfad entsprechend `/HaloCosplay/web/configurator/`. Die Seite benoetigt keine
CDNs, keine Installation und keine Anmeldung. `file://` kann das gemeinsame
JSON-Schema je nach Browser nicht nachladen und wird daher nicht unterstuetzt.

## Bedienung

1. Ein leeres Profil anlegen und einen neutralen Namen vergeben.
2. Ruestungsreferenz, Materialweg, Betriebsart und Ausstattung auswaehlen.
3. Messwerte in mm eintragen. Unbekannte Werte leer lassen. Links und rechts
   bleiben unabhaengig; Schuhmasse am verwendeten Schuh erfassen.
4. Zwischen mehreren Profilen wechseln. Im Konfigurator sind bis zu 100 Profile
   gleichzeitig moeglich. Ein Import fuegt ein Profil hinzu und ersetzt keines.
5. Das aktive Profil als `Profilname.local.json` exportieren. Die Datei kann
   erneut importiert oder vom Python-Werkzeug verarbeitet werden.

Die Demo ist eine ausdrueckliche zweite Aktion. Ihre vollstaendigen Werte sind
synthetisch. Bearbeitung verwandelt sie nicht in echte Messungen. Fuer reale
Messwerte beginnt ein neues Profil leer. Vollstaendige manuelle Eingaben behalten
`measurements_pending`, bis ihre Herkunft ausdruecklich als selbst gemessen
gekennzeichnet wurde. Jede spaetere Messwert-Aenderung setzt `measured` zurueck.

## Datenschutz und Sicherung

Koerperdaten bleiben standardmaessig im Arbeitsspeicher. Ein Neuladen verwirft sie.
JSON-Export sichert das aktive Profil. Eine vorher aktivierte Browser-Speicherung
wird bei erneutem Oeffnen wiederhergestellt; die Einstellung bleibt sichtbar.
Das Deaktivieren entfernt ausschliesslich die Profilkopie dieses Konfigurators,
nicht den Lesefortschritt des Bauhandbuchs oder bereits exportierte Dateien.

Es werden keine Messwerte ueber das Netzwerk gesendet. Lediglich das gemeinsame
Schema und nach ausdruecklicher Auswahl die synthetische Demo werden lokal vom
gleichen Server geladen. Die Browser-Speicherung ist nicht verschluesselt und
fuer andere Personen mit Zugriff auf das Browserprofil zugaenglich. Fehlerhafte
Eingaben werden nicht exportiert oder ueber die letzte gueltige Browserkopie
gespeichert. Importdateien und gespeicherte Sammlungen sind auf 1 MiB begrenzt.

## Gemeinsame Schnittstelle

[ProfileSchema.json](../../Design/Parametric/ProfileSchema.json) definiert
Messfelder, Eingabegrenzen, Zugaben und Bauoptionen. Das Werkzeug verwendet die
gleiche Version wie [Template.json](../../Design/Parametric/Profiles/Template.json)
und [suit_fit.py](../../tools/suit_fit.py). Oberste Metadatenfelder aus importierten
Profilen bleiben beim Export erhalten; unbekannte Mess- und Bauoptionen werden
zurueckgewiesen. Aeltere Profile ohne `build` erhalten explizite Standardoptionen.

Ein aus dem Browser exportiertes Profil laesst sich im Repository beispielsweise
so pruefen; der Pfad ist an den Ablageort des Downloads anzupassen:

```bash
python3 tools/suit_fit.py --profile build/Spartan-01.local.json --out build/Spartan-01
```

Fehlende Messwerte bleiben fehlend. Fuer eine ausdrueckliche Konzeptansicht kann
`--concept` verwendet werden; die Ausgaben dokumentieren dann Ersatzwerte.
Die Auswahl der Ruestungsreferenz erzeugt keine originalgetreue Oberflaeche.
Vollstaendige Eingaben und erfolgreiche Softwarepruefungen sind weder eine
Fertigungsfreigabe noch ein Nachweis fuer Passform, Tragfaehigkeit oder Sicherheit.

## Pruefung

```bash
node --test Tests/Automation/configurator.test.cjs
```

Die Tests decken Eingaben, getrennte Profile/Koerperseiten, Statuswechsel,
synthetische Herkunft, Import, Bauoptionen und den Python-Datenaustausch ab.
