// evonav_loader.js — small bootstrap registered in app_include_js.
//
// Reads frappe.boot.evonav_navbar_hide_js (populated by boot.py) and injects
// it via document.createElement('script') with an idempotency guard.
//
// Why this indirection: app_include_js script tags reliably get DOWNLOADED
// but their IIFE top-level code does not always EXECUTE on natural page
// load in some Frappe environments. Manual createElement('script') always
// runs. So we keep the loader tiny here and let it inject the real payload.
//
// IMPORTANT: if you change this file, rename it (e.g. evonav_loader_v2.js)
// to bust nginx's 1-year asset cache, OR fix the nginx cache headers.

(function () {
    "use strict";
    console.log("[evonav] loader: script executed");

    function inject() {
        if (window.__evonav_navbar_hide_injected) return true;
        var src = window.frappe && frappe.boot && frappe.boot.evonav_navbar_hide_js;
        if (!src) return false;

        var s = document.createElement("script");
        s.textContent = src;
        document.head.appendChild(s);
        window.__evonav_navbar_hide_injected = true;
        console.log("[evonav] loader: navbar_hide payload injected");
        return true;
    }

    // Try immediately — frappe.boot may already be populated.
    if (inject()) return;

    // frappe.boot not ready: poll briefly.
    var attempts = 0;
    var MAX = 200; // 200 × 50ms = 10s ceiling
    var iv = setInterval(function () {
        attempts++;
        if (inject() || attempts >= MAX) clearInterval(iv);
    }, 50);
})();
