# Vokabeln – Inhalte

Die Vokabellisten für die Vokabel-App. Jede Datei in `listen/` ist eine Liste.
Nach jedem Push prüft eine GitHub Action alle Listen und erzeugt `manifest.json` –
die App lädt die Listen dann beim nächsten Start (oder über „Listen jetzt aktualisieren“).

## Neue Liste anlegen

Am einfachsten direkt auf github.com: in den Ordner `listen/englisch/` gehen →
**Add file → Create new file** → z.B. `unit-04-essen.md` → speichern („Commit changes“).

```
---
title: Englisch Unit 4 – Essen
from: de
to: en
profiles: [Hilda]
---
der Apfel = the apple
das Brot = the bread | Tipp: Brötchen = roll
laufen = to run / to walk   # mehrere Antworten mit /
```

- Eine Vokabel pro Zeile: `Deutsch = Fremdsprache`
- `| …` hängt einen Hinweis an, der beim Umdrehen angezeigt wird
- `# …` ist ein Kommentar und wird ignoriert
- `from`/`to`: Sprachcodes (`de`, `en`, `fr`, `es`, `it`, `la`, `ja`) – für Fahne und Vorlesestimme
- Japanisch: Kanji-Wörter als `漢字 / かな` (Lesung zuletzt), Kana-Wörter nur in Kana
- `profiles`: wer die Liste automatisch bekommt; ohne diese Zeile bekommen sie alle
- Ordner (z.B. `englisch/`) werden in der App als Gruppen angezeigt

Lernstand bleibt erhalten, wenn du die rechte Seite oder den Hinweis korrigierst.
Änderst du die linke Seite, gilt das Wort als neu. Gelöschte Zeilen verschwinden aus der App,
der Lernstand bleibt aber gespeichert, falls das Wort zurückkommt.

## Lokal prüfen

```
python3 scripts/build_manifest.py
```

## In der App verbinden

Einstellungen → Vokabeln aus GitHub → Quelle → Repo-Adresse eintragen,
`https://github.com/kryobot/vocab` (das Repo muss öffentlich bleiben).
