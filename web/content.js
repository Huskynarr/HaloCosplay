/* Content map for the MJOLNIR Field Manual web app.
 * Paths are repo-root-relative; app.js prepends the site root.
 * The markdown files remain the single source of truth - this only
 * curates order and friendly titles. */

const CONTENT = {
  // Curated, ordered V3 path for a layperson who wants to move fast.
  journey: [
    { title: "Orientierung", sub: "Wo anfangen", file: "Documentation/Guides/Start-Hier.md" },
    { title: "Variante V3 verstehen", sub: "Was dich erwartet", file: "Documentation/Guides/Varianten.md" },
    { title: "Gesamtsystem", sub: "Module + Stromschienen (mit Diagramm)", file: "Documentation/Guides/V3-Systemarchitektur.md" },
    { title: "Masse nehmen", sub: "Messblatt", file: "Documentation/Guides/Messblatt.md" },
    { title: "Einkaufen", sub: "Direkte Kauflinks", file: "Materials/Einkaufsliste-Links.md" },
    { title: "Exoskelett", sub: "Traggestell V3", file: "Documentation/Guides/Exoskelett.md" },
    { title: "AR-Display / HUD", sub: "Stufen A/B/C", file: "Documentation/Guides/Elektronik-AR-Display.md" },
    { title: "Schubduesen + Nebel", sub: "LEDs, Fogger", file: "Documentation/Guides/Elektronik-Schubduesen.md" },
    { title: "Begleit-Roboter", sub: "Optional, Zukunft", file: "Documentation/Guides/Begleitroboter-Integration.md" },
    { title: "Sicherheit", sub: "Vor dem Tragen lesen", file: "Documentation/Guides/Sicherheit.md" },
    { title: "Con-Checkliste", sub: "Vor dem Auftritt", file: "Documentation/Guides/Checklisten.md" },
  ],

  // Full library, grouped. Every entry points at a real markdown file.
  categories: [
    {
      name: "Planung",
      items: [
        { title: "Komplett-Walkthrough", file: "Documentation/Guides/Komplett-Walkthrough.md" },
        { title: "Varianten", file: "Documentation/Guides/Varianten.md" },
        { title: "Kosten", file: "Documentation/Guides/Kosten.md" },
        { title: "Zeitplan", file: "Documentation/Guides/Zeitplan.md" },
        { title: "Anfaengerfehler", file: "Documentation/Guides/Anfaengerfehler.md" },
        { title: "Messblatt", file: "Documentation/Guides/Messblatt.md" },
        { title: "TODO-Liste", file: "Documentation/TODO.md" },
        { title: "Phasen-Kurzuebersicht", file: "Documentation/Guides/BuildGuide.md" },
      ],
    },
    {
      name: "Bau",
      items: [
        { title: "Foam-Bau (V1)", file: "Documentation/Guides/Foam-Bau.md" },
        { title: "3D-Druck (H2C)", file: "Documentation/Guides/3D-Druck.md" },
        { title: "Klebetechniken", file: "Documentation/Guides/Klebetechniken.md" },
        { title: "Lackierung + Finishing", file: "Documentation/Guides/Lackierung-Finishing.md" },
        { title: "Unteranzug + Befestigung", file: "Documentation/Guides/Unteranzug-Befestigung.md" },
        { title: "Waffen-Prop", file: "Documentation/Guides/Waffen-Prop.md" },
        { title: "Exoskelett (V3)", file: "Documentation/Guides/Exoskelett.md" },
      ],
    },
    {
      name: "Elektronik",
      items: [
        { title: "Elektronik-Uebersicht", file: "Documentation/Guides/ElectronicsGuide.md" },
        { title: "V3-Systemarchitektur", file: "Documentation/Guides/V3-Systemarchitektur.md" },
        { title: "HUD", file: "Documentation/Guides/Elektronik-HUD.md" },
        { title: "AR-Display", file: "Documentation/Guides/Elektronik-AR-Display.md" },
        { title: "Schubduesen + Nebel", file: "Documentation/Guides/Elektronik-Schubduesen.md" },
        { title: "Begleit-Roboter", file: "Documentation/Guides/Begleitroboter-Integration.md" },
        { title: "LED-Effekte", file: "Documentation/Guides/LED-Effekte.md" },
        { title: "Strombudget", file: "Documentation/Guides/Elektronik-Strombudget.md" },
        { title: "Batterie", file: "Documentation/Guides/Elektronik-Batterie.md" },
        { title: "Verdrahtung", file: "Documentation/Guides/Elektronik-Verdrahtung.md" },
        { title: "Luefter", file: "Documentation/Guides/Elektronik-Luefter.md" },
        { title: "Audio / Voice", file: "Documentation/Guides/Elektronik-Audio.md" },
        { title: "Autostart (Pi)", file: "Documentation/Guides/Elektronik-Autostart.md" },
        { title: "Code-Uebersicht", file: "Code/README.md" },
      ],
    },
    {
      name: "Material + Einkauf",
      items: [
        { title: "Einkaufsliste mit Links", file: "Materials/Einkaufsliste-Links.md" },
        { title: "Komponentenliste", file: "Materials/ShoppingList.md" },
        { title: "Material-Ueberblick", file: "Documentation/Guides/Materialien.md" },
        { title: "Schuhe", file: "Materials/Shoes.md" },
        { title: "STL-Quellen", file: "Resources/STL-Quellen.md" },
      ],
    },
    {
      name: "Sicherheit + Convention",
      items: [
        { title: "Sicherheit", file: "Documentation/Guides/Sicherheit.md" },
        { title: "Checklisten", file: "Documentation/Guides/Checklisten.md" },
        { title: "Convention-Regeln", file: "Documentation/Guides/Convention-Regeln.md" },
        { title: "Convention-Alltag", file: "Documentation/Guides/Convention-Alltag.md" },
        { title: "Transport", file: "Documentation/Guides/Transport.md" },
        { title: "Fotoshooting", file: "Documentation/Guides/Fotoshooting.md" },
        { title: "Pflege + Wartung", file: "Documentation/Guides/Pflege-Wartung.md" },
        { title: "Fehlerbehebung", file: "Documentation/Guides/Fehlerbehebung.md" },
      ],
    },
    {
      name: "Referenz",
      items: [
        { title: "Glossar", file: "Documentation/Guides/Glossar.md" },
        { title: "Authentizitaet (Look)", file: "Documentation/Guides/Authentizitaet-Referenz.md" },
        { title: "Best Practices", file: "Documentation/Guides/Best-Practices.md" },
        { title: "Praxis-Tipps (Profi)", file: "Documentation/Guides/Praxis-Tipps-Fortgeschritten.md" },
        { title: "LED-Visor-Forschung", file: "Documentation/Guides/LED-Visor-Forschung.md" },
        { title: "Ideen + Erweiterungen", file: "Design/Designs/IdeasReferences.md" },
      ],
    },
  ],
};

// Files whose tables get a persistent "acquired" checkbox column.
const SHOPPING_FILES = new Set([
  "Materials/Einkaufsliste-Links.md",
  "Materials/ShoppingList.md",
]);
