# DigiByte DigiFacts - WordPress plugin

Part of [DigiByte DigiFacts](../).

Show a random DigiFact - a bite-size fact about DigiByte - on your WordPress site. It changes every minute, and is available in multiple languages. Learn more about DigiFacts [here](https://github.com/DigiNode-Tools/digibyte-digifacts).

## Install

1. Download `digibyte-digifacts.zip` from the [latest release](https://github.com/DigiNode-Tools/digibyte-digifacts/releases).
2. In WordPress, go to **Plugins > Add New Plugin > Upload Plugin**, choose the zip, then **Activate**. (Updating from 1.x? Upload it the same way and choose **Replace current with uploaded** - your settings are kept.)
3. Choose the language in **Settings > DigiFacts**.
4. Add the `[digifacts]` shortcode, or the **DigiByte DigiFacts** block, where you want a DigiFact to appear.

## How it works

- Your site fetches the DigiFacts from https://digifacts.diginode.tools at most once an hour. If they can't be fetched, the last copy is used. If there has never been a copy, nothing is shown - errors are never shown to your visitors.
- The DigiFacts are included in your page, and a small script shows a different one every minute. It works with page caching, and your visitors' browsers don't contact any other site.
- A DigiFact that isn't translated into your chosen language yet is shown in English.
- A small "About DigiByte DigiFacts" link is shown under the DigiFact. You can turn it off in **Settings > DigiFacts**.

## Hiding DigiFacts about your own site

Some DigiFacts are about a particular website or project. If yours is one of them, you'll probably want to hide those DigiFacts on your own site - your visitors are already there.

In **Settings > DigiFacts**, type your project's topic under **Hide topics** - that also hides any DigiFacts about it added in future. Each DigiFact's topic is shown next to it on the [proofreading pages](https://digifacts.diginode.tools/proofread/en/). You can also hide single DigiFacts by their ID (e.g. `digifact-7ttm`, shown on the [proofreading pages](https://digifacts.diginode.tools/proofread/en/)). If your project doesn't have a topic yet, [ask for one](https://github.com/DigiNode-Tools/digibyte-digifacts/issues/new).

## Styling

The DigiFacts use your theme's fonts and colours - the box's border and the "About DigiByte DigiFacts" link automatically match the colour of the DigiFact's text. To change how they look, add CSS in **Appearance > Customize > Additional CSS**, using the classes `.digibyte-digifact`, `.digifact-title`, `.digifact-content`, `.digifact-credit` (the "About DigiByte DigiFacts" link), and `.with-box` (when the Box display option is chosen).

## Not using WordPress?

Use the [embed for any website](../README.md#add-digifacts-to-your-website), or the JSON files directly.

## Releasing a new version

Update the Version in `digibyte-digifacts/digibyte-digifacts.php`, the Stable tag and changelog in `digibyte-digifacts/readme.txt`, then push a tag: `git tag wordpress-v2.0.2 && git push origin wordpress-v2.0.2`. The release (with the zip) is built automatically.

## Licence

GPL-2.0-or-later. Made by Olly Stedall ([@saltedlolly](https://github.com/saltedlolly)) for [DigiNode Tools](https://diginode.tools).
