"""
boot.py — reads Evonav Settings and injects the navbar-hide payload source
plus configured hide-labels into bootinfo. The client-side loader
(evonav_loader.js) reads this and injects the payload via
document.createElement('script').

This indirection exists because app_include_js IIFE execution proved
unreliable in some Frappe environments (see Lesson #10 in README).
"""

import os
import frappe


def get_bootinfo(bootinfo):
    """Extend bootinfo with Evonav config + payload source."""
    try:
        settings = frappe.get_cached_doc("Evonav Settings")
    except frappe.DoesNotExistError:
        # Single doesn't exist yet (pre-install state) — bail silently.
        return
    except Exception:
        # Any other failure: log and bail. Do not break Desk boot.
        frappe.log_error(frappe.get_traceback(), "Evonav boot failed")
        return

    # ── Navbar hide configuration ──────────────────────────────────────────
    if settings.get("enable_navbar_hide"):
        labels_raw = settings.get("navbar_hide_labels") or ""
        labels = [
            line.strip()
            for line in labels_raw.splitlines()
            if line.strip()
        ]
        bootinfo.evonav_navbar_hide_labels = labels

        # Read the payload source from disk and ship it inline.
        # The loader will inject this via createElement('script').
        try:
            payload_path = os.path.join(
                frappe.get_app_path("evonav"),
                "public", "js", "navbar_hide_payload.js",
            )
            with open(payload_path, "r", encoding="utf-8") as f:
                bootinfo.evonav_navbar_hide_js = f.read()
        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "Evonav: failed to load navbar_hide_payload.js",
            )
