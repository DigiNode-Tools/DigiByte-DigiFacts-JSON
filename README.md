# DigiByte DigiFacts

<!-- sponsors:short -->
<a href="https://github.com/sponsors/DigiNode-Tools"><img src="https://img.shields.io/badge/Sponsor%20DigiNode%20Tools-Click%20to%20support%20me-0066CC?style=for-the-badge&labelColor=002352&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI0ZGNEZBMyIgZD0iTTEyIDIxLjM1bC0xLjQ1LTEuMzJDNS40IDE1LjM2IDIgMTIuMjggMiA4LjUgMiA1LjQyIDQuNDIgMyA3LjUgM2MxLjc0IDAgMy40MS44MSA0LjUgMi4wOUMxMy4wOSAzLjgxIDE0Ljc2IDMgMTYuNSAzIDE5LjU4IDMgMjIgNS40MiAyMiA4LjVjMCAzLjc4LTMuNCA2Ljg2LTguNTUgMTEuNTRMMTIgMjEuMzV6Ii8%2BPC9zdmc%2B" alt="Sponsor DigiNode Tools - click to support me"></a>

**Find this useful?** Please consider [sponsoring me on GitHub](https://github.com/sponsors/DigiNode-Tools), so I can devote more time to DigiNode Tools and projects like this one.
<!-- /sponsors:short -->

Bite-size facts about DigiByte, for apps, websites and social media. Available in 12 languages, with live data from the DigiByte blockchain.

**Website:** https://digifacts.diginode.tools/help/

## About DigiFacts

DigiFacts are short facts about DigiByte, designed to be shown in apps and websites and shared on social media, to help people learn about DigiByte.

The original DigiFacts were written by members of the DigiByte community in 2021 ([DigiByte-Core/DigiFacts](https://github.com/DigiByte-Core/DigiFacts)). These DigiFacts are based on them, but have been significantly revised and expanded, translated, and given live data such as the number of DigiByte blocks.

## Using DigiFacts

Each language is a JSON file in three formats:

```
https://digifacts.diginode.tools/<language>/<format>.json
```

For example: https://digifacts.diginode.tools/en/social.json

| Format | Links look like | Best for |
|---|---|---|
| `social` | `Learn more: https://example.com` | Social media, apps, terminals |
| `html` | `Learn more <a href="https://example.com">here</a>.` | Websites |
| `markdown` | `Learn more [here](https://example.com).` | Markdown |

Each file has every fact, in order, each with a `title` (which includes its number, e.g. "DigiFact # 1 - Did you know..."), `content` and `url`. The keys (`digifact1`, `digifact3`, ...) identify each fact and never change, so they aren't always consecutive - use the order of the file, or the number in the title. A fact that isn't translated yet is included in English.

Languages: `en` English, `de` German, `es` Spanish, `fr` French, `hi` Hindi, `it` Italian, `ja` Japanese, `ko` Korean, `nl` Dutch, `pt` Portuguese, `ru` Russian, `zh` Chinese (Simplified). The list is also at https://digifacts.diginode.tools/languages.json, and https://digifacts.diginode.tools/info.json shows each language's progress, the block count used and when the facts were last published.

- Show a random fact, e.g. when the page loads or once a minute.
- Some facts include live data, so fetch the file again every few hours - but not more than once an hour.
- Browsers can fetch the files directly (CORS is allowed).
- For WordPress, there's a [DigiFacts plugin](https://github.com/DigiNode-Tools/DigiByte-DigiFacts-Wordpress-Plugin).

## How DigiFacts are built

Everything is in this repository, so anyone can see exactly how DigiFacts are made:

- The facts are in [`facts/`](facts/), one file per language. [`facts/en.json`](facts/en.json) is the original that the translations are based on.
- A [GitHub Action](.github/workflows/build.yml) runs [`build/build.py`](build/build.py) every hour and whenever the facts change. It checks every file, fills in the live data, and publishes the website on GitHub Pages. If a file has a mistake, nothing is published and the previous version stays live.
- The block count comes from several block explorers (chainz.cryptoid.info, digibyte.io and Atomic Wallet's explorer). The middle value is used, readings that look wrong are ignored, and the count never goes backwards. If no explorer answers, it's estimated from DigiByte's 15 second block time.
- Every run is public on the [Actions tab](https://github.com/DigiNode-Tools/DigiByte-DigiFacts-JSON/actions).

## Contributing

Corrections, new DigiFacts and translations are all welcome. Make a pull request, or [open an issue](https://github.com/DigiNode-Tools/DigiByte-DigiFacts-JSON/issues) if you're not sure how.

To read through the facts in any language, side by side with English, use the [proofreading pages](https://digifacts.diginode.tools/proofread/).

### Fixing or adding a DigiFact

- New DigiFacts are added to `facts/en.json` first. Translations follow - until then, the English version is shown in every language.
- Facts are numbered by their order in `facts/en.json`, so the number isn't part of the text. Give a new fact a new key, one higher than the highest key so far (e.g. `digifact87`), and put it wherever it belongs in the list. Never reuse or rename a key - translations are matched to facts by their key.
- To delete a DigiFact, delete it from `facts/en.json` only. The facts after it are renumbered, and the GitHub Action removes it from the translation files automatically.
- Keep the wording neutral: no marketing, and nothing about price. A single DigiFact telling the community about a DigiByte project and what it does is fine.
- Include at most one link. Put it in `url`, and in all three link fields (`link_social`, `link_html` and `link_md`) - see the existing facts for the format.

### Translating

Each language has its own file in `facts/`, with the same keys as `facts/en.json`. Translate the `_title` at the top of the file (once - it's used for every fact, with `{number}` replaced by the fact's number), then each fact's `content` and three link fields. Leave the `url` as it is. See the [translation guide](translation-guide.md).

### Live data

These can be used in a fact, and are replaced with live values when the website is published:

| Value | Example | Shows |
|---|---|---|
| `$blocks_tot_mil` | 24.3 | The number of DigiByte blocks in millions (rounded down to 0.1 million) |
| `$blocks_tot_cs` | 24,372,537 | The number of DigiByte blocks, with commas |
| `$blocks_tot` | 24372537 | The number of DigiByte blocks |

Translations should use the same values as the English fact.

## Projects using DigiFacts

- [DigiNode Tools](https://diginode.tools) - on the DigiNode Tools website and in the DigiNode Dashboard.

## Disclaimer

DigiFacts are written by the DigiByte community, for the DigiByte community. Please help keep them current and accurate. Always do your own research before using any service or product mentioned in a DigiFact - mentions are not endorsements.

## Licence

MIT - see [LICENSE](LICENSE). Anyone can use DigiFacts, as long as the copyright notice is kept. Based on the [original DigiFacts](https://github.com/DigiByte-Core/DigiFacts) by DigiByte Core (MIT).

DigiFacts are maintained by [DigiNode Tools](https://diginode.tools).
