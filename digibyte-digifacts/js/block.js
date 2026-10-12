/* DigiByte DigiFacts block. It shows the same as the [digifacts] shortcode, rendered by the plugin on your site. */
wp.blocks.registerBlockType("digibyte/digifacts", {
	title: "DigiByte DigiFacts",
	description: "A random DigiFact about DigiByte, which changes every minute.",
	icon: "lightbulb",
	category: "widgets",
	edit: function () {
		return wp.element.createElement(
			"div",
			{ style: { padding: "12px", border: "1px dashed #ccc" } },
			"A random DigiByte DigiFact will appear here. (Choose the language in Settings > DigiFacts.)"
		);
	},
	save: function () {
		return null; // Rendered by the plugin
	}
});
