# Exoskelett und eigener Ruestungstraeger

Das [Projektprofil](Mjolnir-Konfiguration.md) legt fest, ob ein Exoskelett
ueberhaupt zum Aufbau gehoert. Der manuelle Einstieg und der eigene
Ruestungstraeger funktionieren konzeptionell auch ohne aktives Geraet.
Ein Serien-Exoskelett zur Gehunterstuetzung bleibt ein separat auszulegender Ausbau.

## 1. Welche Funktion gebraucht wird

| System | Wirkung | Einsatz im Projekt |
| --- | --- | --- |
| Gepolsterter Ruestungstraeger | Verteilt Ruestungsgewicht zwischen Huefte und Oberkoerper | Grundaufbau, individuell angepasst |
| Aktives Hueft-Exoskelett | Unterstuetzt die Beinbewegung mit eigenen Motoren | Separates Seriengeraet nach Pass- und Integrationsprobe |
| Lasttragendes Ganzkoerper-Exoskelett | Koennte bei entsprechender Konstruktion Last zum Boden fuehren | Nicht Bestandteil des vorliegenden Entwurfs |
| Skeletonics/Pantograph/Stelzen | Vergroessert Reichweite und Silhouette | Keine Basisfunktion; eigener Entwicklungsaufwand und eigener Nachweis |

Ein Wander-Exoskelett traegt nicht automatisch eine schwere Ruestung.
Hypershell schliesst in seinen Safety Guidelines v2.0 Gewichtsabstuetzung,
Balancehilfe und Sturzverhinderung ausdruecklich aus. [Herstellerdokument](https://cdn.shopify.com/s/files/1/0746/6326/4492/files/GL_Hypershell_SafetyGuidelines_v2.0_Printed.pdf?v=1782804835)
Der eigene Traeger bleibt deshalb fuer Ruestungsgewicht verantwortlich; der
Koerper traegt dieses Gewicht weiterhin. Auch Gurte an den Schultern nehmen
reale Kraefte auf, vor allem beim Kippen. Eine Lastverteilung nur anhand der
Bezeichnung H-Harness oder Klettergurt anzunehmen, ist unzureichend.

## 2. Zwei konkrete aktive Integrationskandidaten

Stand der Quellenpruefung: 2026-09-08. Angaben sind modellspezifisch; keine
Kauf- oder Passformzusage. Aktuelle Originalanleitung beim konkreten Geraet pruefen.

| Kandidat | Verifizierte relevante Angaben | Offene Auswahlpunkte |
| --- | --- | --- |
| Hypershell X Series (S) | Handbuch v1.3: Guertelbereich 72-122 cm, Hueftbreite 31-42 cm, Oberschenkellaenge 36-50 cm; zusaetzliche Groessen-/Gewichtstabelle | Original-Messdefinition, Koerpergewicht, Gurtkonflikt, Motor-/Akkufreiraum |
| DNSYS X1 | Herstellerseite: Taille 70-125 cm, Oberschenkelumfang 40-62 cm; S/M/L nach Taille; aktives Hueftsystem | Gewaehlte Groesse, Hersteller-Passprobe, groesster dynamischer Oberschenkelumfang, Akku-Zugang |

Quellen: [Hypershell Handbuch v1.3, Anhang S.46-47](https://cdn.shopify.com/s/files/1/0746/6326/4492/files/EN_Hypershell_XS_Series_UserManual_v1.3_Media.pdf?v=1788775823),
[DNSYS X1 Produkt und Groessenauswahl](https://dnsys.ai/products/dnsys-x1-exoskeleton-every-step-is-a-leap-forward-carbon-carbon-pro).

Koerpergroesse allein entscheidet keine dieser Passfragen. Das Repository
legt **kein Geraet fuer alle Profile** fest. Passmasse und Koerpergewicht
werden direkt nach Herstellerdefinition erhoben, nicht aus Fotos oder anderen
Massen abgeleitet. Jedes Projekt dokumentiert seine eigene Geraeteauswahl.
Die im CAD optional eingeblendeten roten Volumina sind generische Reserven,
keine vermessenen Hypershell-/DNSYS-Komponenten.

DNSYS beschreibt das X1 als Bewegungshilfe fuer Hueftgelenke mit eigener
Bewegungserkennung. Daraus folgt keine Freigabe fuer einen verkleideten
Cosplay-Einsatz. [DNSYS FAQ](https://dnsys.ai/pages/faq)
Herstellerleistungen wie Reichweite, Watt oder Ermuedungsreduktion werden nicht
in ein angeblich tragbares Ruestungsgewicht umgerechnet.

## 3. Eigener passiver Traeger T01

Zwei einstellbare Rueckenstege verbinden eine breite, gepolsterte Hueftauflage
mit der oberen Torsoaufnahme. Seitliche Querfuehrungen tragen nur Schalen und
deren Oeffnungsmechanik. Schultergurte stabilisieren und teilen je nach
Haltung die Last. Ein schwerer Akku wird nahe dem Ruecken/Hueftbereich auf
dem **eigenen** Traeger montiert, nicht am Motorarm des Seriengeraets.

| Bauteil | Konstruktive Absicht | Fertigungsstatus |
| --- | --- | --- |
| Rueckenstege | Flaches, leichtes Metallprofil mit grossflaechiger Kanten-/Druckpolsterung | Querschnitt nach realem Lastfall festlegen |
| Queraufnahme oben/unten | Zwei getrennte Fuehrungsebenen fuer T02 | Lastdaten und Biegesteifigkeit nachweisen |
| Hueftauflage | Breites textiles Tragesystem mit dokumentierten Anbaupunkten | Passprobe vor Materialkauf |
| Schultergurte | Einstellbar, vorn vollstaendig zu oeffnen | Keine geschlossene Halsschlaufe |
| Schalenhalter | Austauschbare mechanische Montageplatten | Druckteile zuerst nur kosmetisch/als Passlehre |
| Gliedmassenhalter | Separate textile Aufhaenger | Kein starres Gestell ueber menschliche Gelenke |

Eine PSA-/Klettergurt-Zertifizierung ist keine Freigabe fuer selbst gebohrte,
verschraubte oder angenaehte Fremdanbauten. Original-Trageprodukte werden nicht
umgebaut; geeignete Hersteller-Anbaupunkte oder ein separat bemessener
Kostuemtraeger sind erforderlich. Ohne realen Lastfall wird kein Aluquerschnitt
oder Filament als fertig bemessen bezeichnet.

## 4. Integrationsraum fuer das Seriengeraet

Das aktive Geraet behaelt seine Originalgurte, Manschetten, Elektronik, Akku
und Firmware. Der Ruestungstraeger hat eigene Befestigungspunkte. Eine
mechanische oder elektrische Kraft-/Datenkopplung ist nicht vorgesehen.

1. Seriengeraet ohne Ruestung passend anlegen und reale Bewegungsraeume aufnehmen.
2. Original-Gurtlage und eigenen Huefttraeger gemeinsam pruefen. Ueberlagern
   sich Druckzonen oder rutschen Gurte, ist dieser Traegeraufbau nicht kompatibel.
3. Motoren, bewegte Hebel, Manschetten, Bedienelemente und Akkuentriegelung als
   Freihaltebereiche im eigenen CAD erfassen, inkl. Bewegung und Wartungszugang.
4. Die Ruestungsschale um diese Bereiche aufteilen. Motoren nicht mit einer
   dichten Verkleidung einschliessen; Hersteller-Lueftung und Temperaturgrenzen
   einhalten. Keine Magnete auf oder unmittelbar an Sensor-/Motorgehaeusen.
5. Kabelschlaufen am eigenen Traeger befestigen; bei jeder Bewegung bleiben
   Gurtverschluss und manuelle Abschaltung erreichbar.
6. Stromlose Passprobe, dann vom Hersteller vorgesehene Funktionsprobe;
   anschliessend gemeinsame Probe unter realer Ruestungslast und Temperatur.

Der Freihalteraum wird gemessen, nicht pauschal mit einem festen Abstand von
z.B. 10 mm als sicher erklaert. Aenderungen an Schale, Polsterung oder Gurtlage
koennen eine neue Probe erforderlich machen.

## 5. Integration erst nach Bestehen dieser Nachweise

| Pruefung | Ergebnis derzeit | Abbruchkriterium |
| --- | --- | --- |
| Originalgeraet passt nach Originalanleitung | Offen | Ausserhalb Herstellerbereich / Passform ungeklaert |
| Eigener Traeger passt zusammen mit Geraet | Offen | Druck, Rutschen oder gegenseitiges Verdraengen |
| Volle benoetigte Bewegung ohne Fremdkontakt | Offen | Schale/Gurt/Kabel beruehrt bewegten Hebel oder Sensor |
| Akku und Abschaltung erreichbar | Offen | Ruestung muss dafuer demontiert werden |
| Bedienung nach Herstelleranleitung | Offen | Ruestung verhindert An-/Ablegen oder Bedienung |
| Getrennter mechanischer Notausstieg | Offen | Beide Systeme blockieren sich beim Oeffnen |
| Geraet im stromlosen Zustand beruecksichtigt | Offen | Ausfall erzwingt Bewegung oder verhindert Befreiung |

Die jeweilige Veranstaltung entscheidet ueber ihren konkreten Einsatz. Eine
pauschale Aussage, alle Motoren seien auf allen Conventions verboten oder alle
passiven Federmechaniken erlaubt, wird nicht uebernommen. Fuer die Werkstatt-
und Passphase ist keine Veranstaltungserlaubnis erforderlich.

## 6. Entscheidungsfolge

Zuerst Masse des ausgewaehlten Profils und Torso-Mockup, dann eigener leichter Traeger.
Parallel kann eine Anprobe der beiden Seriengeraete erfolgen. Ergibt die Probe
eine eindeutige Kompatibilitaet, werden die realen Geraetevolumina aufgenommen
und die Schalen angepasst. Ein Geraet passt erst dann zum Projekt, wenn sowohl
sein Originalbetrieb als auch der getrennte Ruestungseinstieg funktionieren.
Das ist ein optionaler aktiver Ausbau, kein als fertig ausgegebenes DIY-Power-Exo.

Systemzusammenhang: [MJOLNIR-Systementwurf](Mjolnir-Systementwurf.md).
