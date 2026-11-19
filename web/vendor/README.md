# Vendored libraries

Unveraenderte Browser-Builds aus den npm-Paketen, damit die Anleitungsseite
keine Laufzeit-Abhaengigkeit von jsdelivr hat und die Versionen fest sind.

| Datei | Paket | Lizenz | SHA-256 |
| --- | --- | --- | --- |
| `marked-12.0.2.min.js` | `marked@12.0.2` (`marked.min.js`) | MIT, siehe `marked-LICENSE.txt` | `15fabce5b65898b32b03f5ed25e9f891a729ad4c0d6d877110a7744aa847a894` |
| `model-viewer-3.5.0.min.js` | `@google/model-viewer@3.5.0` (`dist/model-viewer.min.js`) | Apache-2.0, siehe `model-viewer-LICENSE.txt` | `8923739c8c1b4a02dd9c8cf66da5c2a448235cb5e49e439dd7bbba944ba4fbe1` |
| `purify-3.4.17.min.js` | `dompurify@3.4.17` (`dist/purify.min.js`) | Apache-2.0 / MPL-2.0, siehe `purify-LICENSE.txt` | `cd37898f9782adf54820c413191b5691803f0f137c799d6edcfd38523b4c2c31` |

Aktualisieren: `npm pack <paket>@<version>`, die genannte Datei kopieren,
Dateiname, `web/index.html` und diese Tabelle anpassen, danach
`node --test Tests/Automation/*.test.cjs` und den Browser-Smoke-Test ausfuehren.

## Tailwind-CSS

`tailwind.css` ist erzeugt (tailwindcss 3.4.17, MIT, siehe `tailwind-LICENSE.txt`)
und enthaelt nur Klassen, die in den Dateien aus `tools/tailwind.config.cjs`
vorkommen. Nach neuen Klassen ab Repository-Wurzel neu bauen:

```bash
npx --yes tailwindcss@3.4.17 -c tools/tailwind.config.cjs -i tools/tailwind.input.css -o web/vendor/tailwind.css --minify
```

Die CI (`suit-design.yml`, Job `browser`) baut das CSS neu und schlaegt fehl, wenn
die eingecheckte Datei abweicht.

Die Datei wird in `web/index.html` nach dem Inline-Stylesheet eingebunden;
diese Reihenfolge entspricht dem frueheren Play-CDN und muss erhalten bleiben.
