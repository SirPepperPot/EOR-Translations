# Contributing EOR translations

## Translation workflow
1. Translate **values** in `languages/<language>.json`, not key names.
2. Compare with `languages/en.json` (the canonical English catalog).
3. Preserve format placeholders such as `{0}` and `{1}`.
4. Submit a pull request and have a maintainer review it.
5. On merge to `main`, GitHub Actions validates the JSON and publishes `manifest.json`.
6. The EOR startup updater downloads approved packs on launch; changes become active on the next launch.

## Language support
- `en.json`: English source (3,669 keys as of initial import)
- `ko.json`: Korean starter (initially empty; falls back to English where supported)
- `pl.json`: Existing partial Polish translations
- `ru.json`: Existing partial Russian translations
- `zh-Hans.json`: Existing Simplified Chinese starter

Legacy Polish and Russian catalogs include old or mismatched entries; the publisher warns about these while requiring new Korean and other language files to match the English key and placeholder format. The mod should always have a reliable English fallback.

## Publication and security
Published files must contain only JSON dictionaries of string keys to string values. The manifest contains SHA-256 hashes; the game updater checks hashes and size limits before replacing files. Do not publish code, DLLs, or game state in language packs.

**Maintainers:** Require pull request review for `main` in GitHub repository settings to prevent unreviewed edits from being published. The website translator interface is a separate future integration.
