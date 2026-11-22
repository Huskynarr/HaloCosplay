# Vendored libraries

Unveraenderte Browser-Builds aus den npm-Paketen, damit die Anleitungsseite
keine Laufzeit-Abhaengigkeit von jsdelivr hat und die Versionen fest sind.

| Datei | Paket | Lizenz | SHA-256 |
| --- | --- | --- | --- |
| `marked-12.0.2.min.js` | `marked@12.0.2` (`marked.min.js`) | MIT, siehe `marked-LICENSE.txt` | `15fabce5b65898b32b03f5ed25e9f891a729ad4c0d6d877110a7744aa847a894` |
| `purify-3.4.17.min.js` | `dompurify@3.4.17` (`dist/purify.min.js`) | Apache-2.0 / MPL-2.0, siehe `purify-LICENSE.txt` | `cd37898f9782adf54820c413191b5691803f0f137c799d6edcfd38523b4c2c31` |

Aktualisieren: `npm pack <paket>@<version>`, die genannte Datei kopieren,
Dateiname, `web/index.html` und diese Tabelle anpassen, danach
`node --test Tests/Automation/*.test.cjs` und den Browser-Smoke-Test ausfuehren.
