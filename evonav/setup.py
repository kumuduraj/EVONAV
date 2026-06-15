"""
setup.py — install/uninstall hooks.

after_install creates the Evonav Settings Single with default hide-labels
("About", "Help", "Frappe Support") and the navbar-hide feature enabled.
"""

import frappe


DEFAULT_HIDE_LABELS = """About
Help
Frappe Support"""


def after_install():
    """Create the Evonav Settings Single with sensible defaults."""
    if not frappe.db.exists("Evonav Settings", "Evonav Settings"):
        doc = frappe.new_doc("Evonav Settings")
        doc.enable_icon_sync = 1
        doc.enable_navbar_hide = 1
        doc.navbar_hide_labels = DEFAULT_HIDE_LABELS
        doc.flags.ignore_permissions = True
        doc.insert()
        frappe.db.commit()


def before_uninstall():
    """Clean up the Single and any cached state."""
    if frappe.db.exists("Evonav Settings", "Evonav Settings"):
        frappe.delete_doc("Evonav Settings", "Evonav Settings", force=True)
    frappe.clear_cache()
