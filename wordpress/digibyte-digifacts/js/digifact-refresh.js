/*
 * DigiByte DigiFacts: show a different random DigiFact every minute.
 * The facts are included in the page by the plugin (window.digibyteDigiFacts), already checked so that the only
 * HTML they contain is a link. With the "Visitor's language" setting, the DigiFacts in the visitor's language are
 * loaded from this site (window.digibyteDigiFactsConfig.url), if available.
 */
(function () {
	"use strict";

	var INTERVAL = 60000; // 60 seconds

	// The best available language for this visitor, e.g. "en-gb", "pt" or "de" - or "" if none is available
	function visitorLanguage(available) {
		var wanted = (navigator.languages && navigator.languages.length) ? navigator.languages : [navigator.language || ""];
		for (var i = 0; i < wanted.length; i++) {
			var code = String(wanted[i] || "").toLowerCase();
			if (available.indexOf(code) >= 0) {
				return code;
			}
			if (available.indexOf(code.split("-")[0]) >= 0) {
				return code.split("-")[0];
			}
		}
		return "";
	}

	// List the DigiFacts this site hides (by topic or ID) in the browser console
	function logHidden(info) {
		if (!info || !info.hidden || !info.hidden.length || !window.console) {
			return;
		}
		var lines = info.hidden.map(function (f) {
			return "#" + f.number + " " + f.id + " (" + f.why + "): " + f.text;
		});
		console.info("DigiFacts: this site hides " + info.hidden.length + " of " + info.total + " DigiFacts\n" + lines.join("\n"));
	}

	function start() {
		var facts = window.digibyteDigiFacts;
		var config = window.digibyteDigiFactsConfig || {};
		logHidden(config.hidden);
		var boxes = document.querySelectorAll(".digibyte-digifact");

		// The "About DigiByte DigiFacts" link: the same colour as the DigiFact's text, whatever colours the theme uses
		for (var b = 0; b < boxes.length; b++) {
			var credit = boxes[b].querySelector(".digifact-credit a");
			var text = boxes[b].querySelector(".digifact-content");
			if (credit && text && window.getComputedStyle) {
				credit.style.color = window.getComputedStyle(text).color;
			}
		}
		if (!facts || !facts.length || !boxes.length) {
			return;
		}

		function showRandom(box) {
			var title = box.querySelector(".digifact-title");
			var content = box.querySelector(".digifact-content");
			var current = title ? title.textContent : "";
			var fact;
			do {
				fact = facts[Math.floor(Math.random() * facts.length)];
			} while (facts.length > 1 && fact.title === current);
			if (title) {
				title.textContent = fact.title;
			}
			if (content) {
				content.innerHTML = fact.content;
			}
		}

		function showAll() {
			for (var i = 0; i < boxes.length; i++) {
				showRandom(boxes[i]);
			}
		}

		setInterval(function () {
			if (!document.hidden) {
				showAll(); // Don't change facts nobody is looking at
			}
		}, INTERVAL);

		// Visitor's language: switch to it straight away, if it's available and not already shown
		if (config.auto && config.url && window.fetch) {
			var lang = visitorLanguage(config.languages || []);
			if (lang && lang !== config.language) {
				fetch(config.url + lang)
					.then(function (r) { return r.ok ? r.json() : null; })
					.then(function (list) {
						if (list && list.length) {
							facts = list;
							showAll();
						}
					})
					.catch(function () { /* Keep showing the DigiFacts already on the page */ });
			}
		}
	}

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", start);
	} else {
		start();
	}
})();
