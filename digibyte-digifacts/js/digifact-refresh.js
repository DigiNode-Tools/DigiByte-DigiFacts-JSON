/*
 * DigiByte DigiFacts: show a different random DigiFact every minute.
 * The facts are included in the page by the plugin (window.digibyteDigiFacts), already checked so that the only
 * HTML they contain is a link.
 */
(function () {
	"use strict";

	var INTERVAL = 60000; // 60 seconds

	function start() {
		var facts = window.digibyteDigiFacts;
		var boxes = document.querySelectorAll(".digibyte-digifact");
		if (!facts || facts.length < 2 || !boxes.length) {
			return;
		}

		function showRandom(box) {
			var title = box.querySelector(".digifact-title");
			var content = box.querySelector(".digifact-content");
			var current = title ? title.textContent : "";
			var fact;
			do {
				fact = facts[Math.floor(Math.random() * facts.length)];
			} while (fact.title === current);
			if (title) {
				title.textContent = fact.title;
			}
			if (content) {
				content.innerHTML = fact.content;
			}
		}

		setInterval(function () {
			if (document.hidden) {
				return; // Don't change facts nobody is looking at
			}
			for (var i = 0; i < boxes.length; i++) {
				showRandom(boxes[i]);
			}
		}, INTERVAL);
	}

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", start);
	} else {
		start();
	}
})();
