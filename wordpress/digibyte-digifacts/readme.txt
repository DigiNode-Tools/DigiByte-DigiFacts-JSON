=== DigiByte DigiFacts ===
Contributors: saltedlolly
Donate link: https://github.com/sponsors/DigiNode-Tools
Tags: digibyte, digifacts, crypto, blockchain
Requires at least: 5.0
Tested up to: 6.8
Stable tag: 2.2.3
Requires PHP: 7.4
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Show a random DigiFact - a bite-size fact about DigiByte - that changes every minute. Available in multiple languages.

== Description ==

DigiFacts are short facts about DigiByte, to help people learn about it. This plugin shows a random DigiFact on your site, and changes it every minute. Some DigiFacts include live data, such as the number of DigiByte blocks.

Choose the language in Settings > DigiFacts. A DigiFact that isn't translated yet is shown in English. If your site or project is mentioned in some DigiFacts, you can hide those on your own site - by topic or by ID. Learn more about DigiFacts at https://github.com/DigiNode-Tools/digibyte-digifacts

== Usage ==

Add the [digifacts] shortcode, or the DigiByte DigiFacts block, where you want a DigiFact to appear.

== How it works ==

* The DigiFacts are fetched from https://digifacts.diginode.tools by your site, at most once an hour. If they can't be fetched, the last copy is used. If there has never been a copy, nothing is shown.
* The DigiFacts are included in your page, and a small script shows a different one every minute. It works with page caching, and your visitors' browsers don't contact any other site.

== Screenshots ==

1. DigiFacts settings - choose the language, and whether the DigiFact is shown in a box.
2. A DigiFact on a website.

== Changelog ==

= 2.2.3 =
* The box and the About link fit your site's colours automatically, and your own CSS can still change them.
* Your own CSS now always takes priority over the plugin's (its small stylesheet loads first, in the page's head).

= 2.2.2 =
* The box around the DigiFact is visible again on sites with a dark background (its border now uses the colour of the DigiFact's text, as the About link does).

= 2.2.1 =
* The "About DigiByte DigiFacts" link is the same colour as the DigiFact's text, whatever colours your theme uses.

= 2.2.0 =
* A small "About DigiByte DigiFacts" link under the DigiFact, like the DigiFacts embed. You can turn it off in Settings > DigiFacts.
* The settings explain what hiding DigiFacts is for: hiding the DigiFacts about your own site or project.
* Hide topics: type your project's topic (it's shown on the DigiFacts proofreading pages), instead of choosing from a list. Your current setting is kept.

= 2.1.2 =
* DigiFact IDs are now like digifact-7ttm, so they can't be mistaken for DigiFact numbers. If you hid DigiFacts by ID, please enter their new IDs, from the proofreading pages.

= 2.1.1 =
* The settings page always shows the latest languages and topics, and saving the settings applies them straight away.

= 2.1.0 =
* Visitor's language: show each visitor the DigiFacts in their browser's language, if available.
* Hide DigiFacts on your site: by topic (e.g. DigiFacts about your own project) or by ID, in Settings > DigiFacts.

= 2.0.1 =
* The plugin now lives in the DigiFacts repository: https://github.com/DigiNode-Tools/digibyte-digifacts

= 2.0.0 =
* Uses the new DigiFacts website (digifacts.diginode.tools), which is now built and published openly on GitHub.
* No more AJAX or jQuery: the DigiFacts are included in the page, so they work with page caching.
* Several DigiFacts on one page now change independently.
* Language names are shown in the settings.
* Errors are never shown to your visitors. If the DigiFacts can't be loaded, the last copy is used.
* Deleting the plugin removes everything it stored.

= 1.1 =
* Initial release

== Upgrade Notice ==

= 2.0.0 =
Required: the old DigiFacts web service has been replaced, and version 1.x can only show English DigiFacts from it.
