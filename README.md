# DigiByte DigiFacts - WordPress plugin

<!-- sponsors:short -->
<a href="https://github.com/sponsors/DigiNode-Tools"><img src="https://img.shields.io/badge/Sponsor%20DigiNode%20Tools-Click%20to%20support%20me-0066CC?style=for-the-badge&labelColor=002352&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI0ZGNEZBMyIgZD0iTTEyIDIxLjM1bC0xLjQ1LTEuMzJDNS40IDE1LjM2IDIgMTIuMjggMiA4LjUgMiA1LjQyIDQuNDIgMyA3LjUgM2MxLjc0IDAgMy40MS44MSA0LjUgMi4wOUMxMy4wOSAzLjgxIDE0Ljc2IDMgMTYuNSAzIDE5LjU4IDMgMjIgNS40MiAyMiA4LjVjMCAzLjc4LTMuNCA2Ljg2LTguNTUgMTEuNTRMMTIgMjEuMzV6Ii8%2BPC9zdmc%2B" alt="Sponsor DigiNode Tools - click to support me"></a>

**Find this useful?** Please consider [sponsoring me on GitHub](https://github.com/sponsors/DigiNode-Tools), so I can devote more time to DigiNode Tools and projects like this one.
<!-- /sponsors:short -->

Show a random DigiFact - a bite-size fact about DigiByte - on your WordPress site. It changes every minute, and is available in multiple languages. Learn more about DigiFacts [here](https://github.com/DigiNode-Tools/DigiByte-DigiFacts-JSON).

## Install

1. Download `digibyte-digifacts.zip` from the [latest release](https://github.com/DigiNode-Tools/DigiByte-DigiFacts-Wordpress-Plugin/releases/latest).
2. In WordPress, go to **Plugins > Add New Plugin > Upload Plugin**, choose the zip, then **Activate**. (Updating from 1.x? Upload it the same way and choose **Replace current with uploaded** - your settings are kept.)
3. Choose the language in **Settings > DigiFacts**.
4. Add the `[digifacts]` shortcode, or the **DigiByte DigiFacts** block, where you want a DigiFact to appear.

## How it works

- Your site fetches the DigiFacts from https://digifacts.diginode.tools at most once an hour. If they can't be fetched, the last copy is used. If there has never been a copy, nothing is shown - errors are never shown to your visitors.
- The DigiFacts are included in your page, and a small script shows a different one every minute. It works with page caching, and your visitors' browsers don't contact any other site.
- A DigiFact that isn't translated into your chosen language yet is shown in English.

## Styling

The DigiFacts use your theme's fonts and colours. To change how they look, add CSS in **Appearance > Customize > Additional CSS**, using the classes `.digibyte-digifact`, `.digifact-title`, `.digifact-content`, and `.with-box` (when the Box display option is chosen).

## Not using WordPress?

The DigiFacts are available as JSON files for any website or app - see [DigiByte-DigiFacts-JSON](https://github.com/DigiNode-Tools/DigiByte-DigiFacts-JSON).

## Licence

GPL-2.0-or-later. Made by Olly Stedall ([@saltedlolly](https://github.com/saltedlolly)) for [DigiNode Tools](https://diginode.tools).
