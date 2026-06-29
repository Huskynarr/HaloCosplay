# Bauteil-Fotos fuer den 3D-Viewer

Der 3D-Viewer zeigt im Bauteil-Panel optional ein Referenzfoto je Komponente.
Lege dafuer Bilder unter diesem Namen ab:

```
web/img/parts/<id>.jpg
```

Gueltige `<id>`-Werte (passend zu den Markern im Viewer):

| id        | Bauteil                     |
|-----------|-----------------------------|
| helm      | Helm                        |
| visier    | Visier                      |
| hud       | HUD im Helm                 |
| brust     | Brustpanzer                 |
| schulter  | Schulterpanzer              |
| arm       | Unterarm / Gauntlet         |
| hand      | Handschuhe + Unteranzug     |
| bein      | Oberschenkel + Beinpanzer   |
| stiefel   | Stiefel / Schienbein        |
| akku      | Akku + Elektronik           |
| exo       | Exoskelett                  |

Hinweise:
- Format `.jpg`, moeglichst quer (Querformat sieht im Panel am besten aus).
- Fehlt ein Bild, blendet sich der Foto-Slot automatisch aus - kein kaputtes
  Bildsymbol. Du musst also nicht alle Fotos auf einmal liefern.
- Eigene Baufotos sind ideal (zeigen deinen echten Fortschritt). Achte bei
  fremden Bildern auf die Lizenz.
