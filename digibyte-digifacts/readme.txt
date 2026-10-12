=== DigiByte DigiFacts ===
Contributors: saltedlolly
Donate link: https://github.com/sponsors/DigiNode-Tools
Tags: digibyte, digifacts, crypto, blockchain
Requires at least: 5.0
Tested up to: 6.8
Stable tag: 2.0.0
Requires PHP: 7.4
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Show a random DigiFact - a bite-size fact about DigiByte - that changes every minute. Available in multiple languages.

== Description ==

DigiFacts are short facts about DigiByte, to help people learn about it. This plugin shows a random DigiFact on your site, and changes it every minute. Some DigiFacts include live data, such as the number of DigiByte blocks.

Choose the language in Settings > DigiFacts. A DigiFact that isn't translated yet is shown in English. Learn more about DigiFacts at https://github.com/DigiNode-Tools/DigiByte-DigiFacts-JSON

== Usage ==

Add the [digifacts] shortcode, or the DigiByte DigiFacts block, where you want a DigiFact to appear.

== How it works ==

* The DigiFacts are fetched from https://digifacts.diginode.tools by your site, at most once an hour. If they can't be fetched, the last copy is used. If there has never been a copy, nothing is shown.
* The DigiFacts are included in your page, and a small script shows a different one every minute. It works with page caching, and your visitors' browsers don't contact any other site.

== Screenshots ==

1. DigiFacts settings - choose the language, and whether the DigiFact is shown in a box.
2. A DigiFact on a website.

== Changelog ==

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
