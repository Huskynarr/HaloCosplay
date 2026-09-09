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

## 2. Konkreter preiswerter Displayversuch

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

Als Alternative zu selbst aufgebauter Optik kann ein vollstaendiges kommerzielles
Near-Eye-System auf Platz und SDK geprueft werden. Beispielsweise dokumentiert
Vuzix fuer Z100 eine Mobilgeraeteanbindung und ein Android-SDK zur Ausgabe von
Text und Bildern. Das ist eine eigene Integration; der vorhandene OLED-Code
laeuft darauf nicht unveraendert. Fuer diese Option liegt hier weder ein
aktuelles Kaufangebot noch eine Helm-Passprobe vor.
[Vuzix SDK](https://support.vuzix.com/docs/sdk-for-android)

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
