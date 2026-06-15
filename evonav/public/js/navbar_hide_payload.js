// navbar_hide_payload.js — runs after being injected by evonav_loader.js.
//
// Hides navbar items whose visible text matches any label configured in
// Evonav Settings (default: "About", "Help", "Frappe Support").
//
// Uses a MutationObserver because Frappe's navbar renders dropdown items
// lazily — items may appear after page load when the user opens a menu.
// The observer keeps the hidden state enforced.
//
// Idempotency: window.__evonav_navbar_hide_installed prevents double-attach
// if this payload is injected more than once.

(function () {
    "use strict";
    var DEBUG = false;

    if (window.__evonav_navbar_hide_installed) return;
    window.__evonav_navbar_hide_installed = true;

    var labels = (frappe && frappe.boot && frappe.boot.evonav_navbar_hide_labels) || [];
    if (!labels.length) {
        if (DEBUG) console.log("[evonav] navbar_hide: no labels configured, skipping");
        return;
    }

    // Normalize for case-insensitive matching.
    var lowerLabels = labels.map(function (l) { return l.toLowerCase().trim(); });

    function hideMatchingItems() {
        // Selectors cover the common navbar element types in Frappe v15/v16.
        var selectors = [
            ".navbar a",
            ".navbar .dropdown-item",
            ".dropdown-menu a",
            ".dropdown-menu .dropdown-item",
            "header .nav-link",
            ".navbar-nav .nav-item a",
        ];
        var nodes = document.querySelectorAll(selectors.join(","));
        nodes.forEach(function (el) {
            if (el.dataset.evonavHidden === "true") return; // already hidden
            var text = (el.textContent || "").trim().toLowerCase();
            if (!text) return;
            if (lowerLabels.indexOf(text) !== -1) {
                el.style.display = "none";
                el.setAttribute("data-evonav-hidden", "true");
                // Hide the wrapping <li> if present so the gap also collapses.
                var li = el.closest("li");
                if (li) li.style.display = "none";
            }
        });
    }

    // Initial sweep.
    hideMatchingItems();

    // Re-sweep on any DOM mutation (dropdowns load lazily).
    var observer = new MutationObserver(function () {
        hideMatchingItems();
    });
    observer.observe(document.body, { childList: true, subtree: true });

    // Also re-sweep on every Frappe route change (extra safety).
    // Guard for v16 API: frappe.router.on may be frappe.router.events.on.
    try {
        if (window.frappe && frappe.router) {
            var router = frappe.router.events || frappe.router;
            if (router.on) router.on("change", hideMatchingItems);
        }
    } catch (e) { /* router hook not critical */ }

    if (DEBUG) console.log("[evonav] navbar_hide: installed with labels =", labels);
})();
