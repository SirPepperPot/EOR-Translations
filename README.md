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
