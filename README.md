# EOR Translations

Community-managed localization packs for Enhanced Overhaul Remix (For The King II).

| Language | Pack |
| --- | --- |
| Korean | `ko` |
| Polish | `pl` |
| Russian | `ru` |
| Simplified Chinese | `zh-Hans` |

Use an EOR build that includes GitHub translation cache support. The updater
checks this repo's `manifest.json` in the background at startup. Any new
packs apply on the **next launch**. Previously downloaded packs work offline,
and missing entries fall back to installed text or English. Coverage is partial
and varies by language.

Set the game's language or use EOR's `[Localization] Language` setting. To turn off
network checks without removing cached packs, set `[Translations] AutoUpdate = false`
in `BepInEx/config/sirpepperpot.eor.translation-updater.cfg`.

See [CONTRIBUTING.md](CONTRIBUTING.md) to submit translation fixes. English is
maintained in the main EOR repository. Submit only translated values, keeping
the original keys and numbered placeholders intact.

## Bulk translation with Google Translate

[Download the EOR Translation Workbench](https://raw.githubusercontent.com/SirPepperPot/EOR-Translations/main/tools/EOR-Translation-Workbench.html)
and save it as an `.html` file. Open it in Opera, Chrome, Edge, or another
current Chromium browser on your PC. The workbench runs locally with no
installation, API key or sign-in.

1. Select a target language. Load [the English catalog](languages/en.json)
   and, if that language already has a pack, load its JSON file too. The
   workbench keeps existing translations with valid placeholders.
2. Download the spreadsheet. Drag it into
   [Google Translate Documents](https://translate.google.com/?op=docs),
   choose English and the same target language, then translate and download it.
   Google takes one target language per upload.
3. Drop Google's downloaded XLSX into the workbench and save the resulting
   language JSON. If you closed the workbench, reload the same English catalog,
   target language and existing pack first.

JSON keys are never sent to Google. The workbench checks row IDs and
formatting tokens, including numbered placeholders and Crownfall's
`{{QUEST_COMPLETION_TRACKER}}`. If a line is blank, unchanged, or has damaged
tokens, the workbench leaves that entry out of the draft and lists it in a
downloadable review report. Check that the language is correct and spot-check
terminology before publishing. The workbench does not publish anything.

The workbench prepares files for every FTK2 interface language. The four
languages listed above are currently the only packs the EOR updater delivers.
