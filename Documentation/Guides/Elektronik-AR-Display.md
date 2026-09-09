# Elektronik: HUD, transparentes Display und AR im Helm

Die vorgesehene Basis ist ein optisch durchsichtiges Visier. Ein optionales,
seitlich angeordnetes und von Hand wegklappbares monokulares HUD ergaenzt kleine
Statusanzeigen. Kamera und Anzeige ersetzen beim Gehen nicht die direkte Sicht.
Die genaue Einbaulage beschreibt [Helmintegration](Mjolnir-Helmintegration.md).

## 1. Transparent ist noch kein lesbares HUD

Ein transparentes OLED ist eine echte Anzeige, aber kein fertiges Near-Eye-System.
Wenige Zentimeter vor dem Auge lassen sich seine Pixel normalerweise nicht
bequem scharfstellen. Fuer ein virtuell weiter entferntes Bild werden passende
Abbildungsoptik, Augenabstand und Justage benoetigt. Ein einfacher transparenter
Spiegel allein loest das Fokusproblem nicht. Das ist auch die zentrale Aufgabe
von Near-Eye-Optiken in der [optischen Fachliteratur](https://www.nature.com/articles/s41377-024-01674-0).

| Ausfuehrung | Wirkung | Entscheidung fuer dieses Projekt |
| --- | --- | --- |
| Kleine Anzeige als sichtbare Helm-Dekoration | Pixel sind von aussen oder auf dem Tisch sichtbar; Lesbarkeit am Auge offen | Guenstiger Effektversuch, ausserhalb des zentralen Sichtfensters |
| Monokulares HUD mit Abbildungsoptik und Combiner | Kleine Information scheinbar vor der realen Umgebung | Optionaler Ausbau nach optischer Passprobe |
| Ganzflaechige transparente Scheibe ohne Optik | Kein automatisch scharfes oder raeumlich verankertes Bild | Kein vorgesehener AR-Ersatz |
| Kamera-Passthrough mit augennaher Anzeige | Direkte Sicht wird durch Video ersetzt | Getrennter stationaerer Demonstrator |

Auch ein transparentes Display reduziert oder veraendert die Durchsicht durch
Rahmen, Leiterbahnen, Tinte, Reflexionen und leuchtende Bildinhalte. Die fruehere
pauschale Zusage einer vollstaendig erhaltenen Sicht entfaellt.

## 2. Fertige Near-Eye-Optik als bevorzugter Ausbau

Stand der Herstellerrecherche: 2026-09-09. Fuer das funktionsfaehige Helm-HUD
wird ein komplettes optisches System mit Treiber bevorzugt. Ein hoeheres
Displaybudget ist vorgesehen; die folgende Auswahl ist noch keine Bestellung
oder bestaetigte mechanische Integration.

| Kandidat | Belegte Herstellerangaben | Einordnung und offene Punkte |
| --- | --- | --- |
| [ENMESI R3](https://www.enmesi.com/sale-12375134-mipi-1920-1080-type-c-micro-lcd-display-module-for-augmented-reality-wearable.html) | LCOS-Waveguide, 1920 x 1080, 40 Grad FOV, 60 Hz; angegebene Transmission ueber 82 Prozent; Controller Type-C, internes Panel MIPI | Interessant fuer eine eigene Helmkassette. Preis verhandelbar, Mindestmenge 50 Stueck. Einzelmuster, vollstaendiger optischer Lieferumfang und Videoeingangsprotokoll unbestaetigt. |
| [XREAL One Pro](https://www.xreal.com/one-pro) | Fertige Farb-Displaybrille, 57 Grad FOV, bis 120 Hz; USB-C mit DisplayPort-Ausgabe an der Quelle erforderlich | Praktischer Kandidat fuer einen ersten vollstaendigen HUD-Versuch. Zunaechst unzerlegt testen; Brillenrahmen, Tasten und Kabel muessen unter den Helm passen. |

Der [XREAL EU-Shop](https://eu.shop.xreal.com/products/xreal-one-pro) zeigte
599 EUR inklusive Steuern, statt 689 EUR. Der Abruf enthielt sowohl Kauf- als
auch Nachlieferungsanzeigen; Bestand der passenden Variante ist damit nicht
bestaetigt. Versand und gegebenenfalls Sehhilfen kommen separat hinzu.
Die Produktseite unterscheidet IPD-Varianten 57-66 und 66-75 mm; die passende
Variante folgt der Messung und Passprobe.

Beim R3 ist die Angabe "Pupil Distance 18mm" nicht eindeutig definiert und wird
nicht als Augenabstand eines Menschen uebernommen. Ebenso beschreibt die
Panel-Leistungsangabe nicht automatisch den Verbrauch von Beleuchtung,
Controller und kompletter Optik. Diese Werte bleiben im Energieplan unbekannt.
Alle genannten optischen Werte sind Herstellerangaben, keine Messungen am Helm.

AliExpress bleibt ein moeglicher Beschaffungskanal. Ein konkretes Angebot mit
bestaetigtem Lieferumfang und Einzelstueckpreis konnte nicht verifiziert werden.
Suchbegriffe: `optical see through AR module driver board`, `LCOS waveguide
module evaluation kit`, `monocular HUD optical engine HDMI`. Ein als AR
beworbenes Micro-OLED oder ein Kamerasucher kann die Umgebung verdecken;
"AR" im Titel belegt keine Durchsicht.

### 2.1 Beschaffung und Budget

Als eigene Planungsreserve werden **800-1200 EUR fuer einen Display-Prototyp**
angesetzt, inklusive Optik/Brille, kompatibler Videoquelle beziehungsweise
Adapter, Halter und Verkabelung. Das ist kein OEM-Angebot und umfasst keine
kundenspezifische Waveguide-Entwicklung. Vorhandene geeignete Rechner koennen
Kosten senken. Das generische Projektbudget wird erst nach Auswahl mit dem
realen Preis und gemessenen Leistungsbedarf befuellt.

Vor einem OEM-Muster muessen folgende Angaben vorliegen:

- Exakte Artikelrevision, Einzelmusterpreis, Mindestmenge und Lieferzeit;
  Aufstellung von Optik, Beleuchtung, Controller, Firmware und Kabeln.
- Optische Durchsicht, Farbe, nutzbare Eyebox, Eye Relief, virtuelle Bildweite,
  Helligkeit am Auge und Regelbereich; Zeichnungen mit Befestigungspunkten.
- Tatsaechlicher Videoeingang und unterstuetzte Aufloesungen. Type-C alleine
  bestaetigt weder DisplayPort noch USB-Video. MIPI benoetigt einen passenden
  Controller und ist kein beliebiger HDMI-Anschluss.
- Versorgung, Einschaltspitze, Dauerverbrauch und Temperaturgrenzen des
  kompletten Systems; Wiederanlauf nach Kabel- und Stromunterbrechung.

### 2.2 Integration in den Halo-Helm

Der erste Versuch zeigt ein sparsames farbiges Halo-HUD: Schildbalken als
kenntliche Inszenierung sowie echte Batterie-, Temperatur- und Modusdaten.
Schwarzer Bildhintergrund reduziert leuchtende Flaechen, beseitigt aber weder
Brillentint noch optische Verluste. Goldvisier und Brille werden gemeinsam auf
Durchsicht, Reflexionen und Beschlag geprueft.

Host und grosse Energiequelle sitzen vorzugsweise im Torso; im Helm bleiben
Optik und erforderliche Treiber. Kabel benoetigen Zugentlastung und eine
loesbare Verbindung fuer das Abnehmen. Bei einer kompletten Brille werden
zunaechst deren Originalrahmen und optische Justage erhalten. Eine wegklappbare
OEM-Kassette folgt erst aus deren realer Geometrie und Eyebox.

Eine Quelle mit USB-C-DP-Ausgang kann die XREAL direkt ansteuern. Bei HDMI ist
ein aktiver, ausdruecklich fuer HDMI-Quelle zu USB-C-Display geeigneter und
versorgter Adapter erforderlich; ein ueblicher USB-C-zu-HDMI-Adapter ist nicht
umkehrbar. Diese Kombination ist vor Einbau am Tisch zu pruefen.

Der bestehende I2C-OLED-Code ist kein Farb-HDMI-/DP-Renderer. Ein passender
Renderer mit Telemetrieanbindung, Ausfallanzeige fuer veraltete Messwerte und
geprueftem Startverhalten bleibt Implementierungsarbeit nach Hardwareauswahl.
Die Konfiguratoroption `hud=combiner` waehlt bisher nur ein Einbaukonzept;
sie erzeugt keine XREAL-/R3-Treiber, CAD-Passform oder verifizierte Leistungsdaten.

### 2.3 Preiswerter Displayversuch als separate Option

**Waveshare 1.51inch Transparent OLED**: SSD1309, 128 x 64 Pixel, monochrom
hellblau; aktive Flaeche 35.05 x 15.32 mm, Treiberplatine 41 x 22.5 mm.
Das Modul unterstuetzt SPI und I2C bei 3.3/5 V Versorgung. Werkseitig ist
Vierdraht-SPI gewaehlt; fuer I2C muessen laut Hersteller zwei 0-Ohm-Widerstaende
umgesetzt werden. Anschluss- und Resetkonfiguration sind vor dem Betrieb zu
pruefen. [Waveshare-Dokumentation](https://www.waveshare.net/wiki/1.51inch_Transparent_OLED)

Die [Hersteller-Produktseite](https://www.waveshare.com/1.51inch-transparent-oled.htm)
wurde am 2026-09-09 mit 19.99 USD und ohne Lagerbestand im Suchindex gefunden;
der direkte Abruf war gesperrt. Das ist eine Preisorientierung, kein verfuegbares
Angebot und kein deutscher Endpreis. Optik, Halter, Rechner, Versand und Abgaben
sind nicht enthalten. Eine RGB-Anzeige oder ein grosses Visier entsteht daraus
nicht.

Der vorhandene [HUD-Code](../../Code/HelmetControl/hud_display.py) zeichnet ein
128-x-64-Bild und benutzt I2C. Er ist damit nicht automatisch kompatibel mit dem
SPI-Auslieferungszustand. Ein erfolgreicher PNG-Selbsttest prueft weder Anschluss,
Resetsequenz, sichtbaren Bildausschnitt noch Lesbarkeit im Helm. Der
[HUD-Inbetriebnahmeguide](Elektronik-HUD.md) trennt diese Schritte.

## 3. Monokulares HUD als ausbaubares Modul

Die mechanische Entwicklungsrichtung ist ein kleines Modul seitlich oberhalb
der normalen Blickachse. Links oder rechts wird nach Passprobe entschieden;
Augendominanz allein bestimmt die Position nicht. Das zentrale Sichtfenster und
der Blick auf Boden und Stufen bleiben frei. Display, Linse und gegebenenfalls
Combiner werden gemeinsam justiert und danach gegen Verstellen gesichert.

Noetige Eigenschaften:

- Einstellbare Hoehe, seitliche Lage, Neigung und optischer Abstand; Brille und
  Wimpern duerfen bei Kopfbewegung keinen Kontakt bekommen.
- Definierte wegklappbare Parkposition, die ohne Strom und mit Handschuhen
  erreichbar ist; Kabelschlaufe ausserhalb der Klemmstellen.
- Kleine Statusflaeche statt dauernd gefuelltem Bild; Helligkeit von dunkel aus
  einstellen, Reflexe bei geschlossenem und offenem Visier vergleichen.
- Abgerundete Einfassung des optischen Bauteils und mechanische Sicherung; ein
  loses Displayglas gehoert nicht unmittelbar vor das Auge.

Vor Detail-CAD sind der nutzbare Augenraum, die Austrittspupille beziehungsweise
Eyebox des gewaehlten Optikmoduls, Scharfstellbereich und Sichtfeld zu erproben.
Ein pauschaler Montageabstand von 3-5 cm ersetzt diese Angaben nicht. Eine
beliebige Lupe oder ein Prisma wird deshalb nicht als fertiges Kaufrezept
festgelegt.

## 4. HUD-Funktion und echte AR unterscheiden

Batteriestatus, Temperaturen, Betriebsmodus oder ein inszenierter Schildbalken
brauchen keine AR. Eine tatsaechlich an der Umgebung verankerte Markierung
braucht dagegen kalibrierte Optik, Lageverfolgung und ein geeignetes
Koordinatensystem. Ein IMU-Kompass oder Kamera-Overlay alleine liefert das nicht.

Die vorhandenen Demo-Anzeigen bleiben als Simulation kenntlich. Ein gruener
Videofilter ist keine Nachtsicht, digitaler Zoom erzeugt keine zusaetzlichen
Bilddetails und allgemeine Personenerkennung ist keine Freund-Feind-Erkennung.
Solche Funktionen gehoeren nicht zur zugesagten Helm-Ausstattung.

## 5. Kamera-Passthrough bleibt ein eigener Demonstrator

[Code/HelmetControl/AR](../../Code/HelmetControl/AR/README.md) enthaelt eine
Kamera-/Overlay-Demonstration. Der Code misst aktuell die Zeit um den
Kameraabruf vor Overlay und Anzeige. Die dort dargestellten Latenz-/FPS-Werte
sind deshalb **kein Nachweis der End-to-End-Latenz oder der sichtbaren Bildrate**.
Belichtung, interne Puffer, Bildverarbeitung und Displayausgabe muessen fuer
eine solche Messung mit erfasst werden. Ein Warnbanner hilft zudem nicht bei
Stromausfall, blockierter Software oder ausgefallenem Bildschirm.

Es gibt hier keinen nachgewiesenen Grenzwert, ab dem das Gehen mit diesem
Eigenbau freigegeben waere. Ein leistungsstaerkerer Rechner, CSI oder 60 fps
alleine liefern diese Freigabe ebenfalls nicht. Die Wahl des Rechners folgt
der gemessenen kompletten Pipeline und dem Waermebudget.

Fuer einen stationaeren Demonstrator gelten direkte mechanische Freisicht ohne
Strom, erreichbare Helm-/Visierentriegelung und eine begleitende Person beim
Versuch. Realsicht wird vor Ortswechsel wiederhergestellt. Der alltagstaugliche
Projektpfad bleibt das durchsichtige Visier mit optionalem kleinen HUD.
