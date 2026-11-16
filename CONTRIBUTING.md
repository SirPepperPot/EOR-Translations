# Contributing EOR translations

1. Use [languages/en.json](languages/en.json) as the template.
2. In your language's JSON, keep each key unchanged and translate its value. Leave unfinished keys out so EOR can fall back to its shipped text.
3. Keep numbered placeholders such as `{0}` and `{1}`, including any numeric formatting. You can reorder placeholders to fit the language. Keep rich-text tags and intentional line breaks.
4. Open a pull request. After merge, GitHub Actions validates the packs and publishes their hashes in `manifest.json`.
5. EOR follows the game language by default. The updater downloads changed packs in the background and they take effect on the next launch.

The template includes EOR labels, descriptions, menus, HUD text, campaign objectives and Crownfall dialogue, including keys for generated spells and followers. It does not replace vanilla game translations. For legendary item descriptions, keep the English section-marker syntax or use the matching translated values of `EOR_CODEX_LEGENDARY_EFFECT_MARKER` and `EOR_CODEX_LEGENDARY_FLAVOR_MARKER`.

Korean, Polish, Russian, and Simplified Chinese packs are partial. The validator reports legacy Polish and Russian keys needing cleanup. Maintainers should copy new English source from the main mod's shipped `Runtime/EnhancedOverhaulRevamped/Localization/en.json`.
