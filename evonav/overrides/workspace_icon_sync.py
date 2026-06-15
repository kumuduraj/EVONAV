"""
workspace_icon_sync.py — keeps the workspace sidebar icon in sync.

Background
----------
Frappe Workspace has a built-in `icon` field but in some versions the
icon set there doesn't render reliably in the sidebar after edits without
a cache clear. This module:

  1. Adds a parallel custom field `evonav_workspace_icon` (Data) on
     Workspace via fixtures (see fixtures/custom_field.json).
  2. On every Workspace `on_update`, copies the value from
     `evonav_workspace_icon` to the standard `icon` field.
  3. Clears the workspace sidebar cache so the new icon appears
     immediately on the next page load (no bench restart needed).

Disabling
---------
Set Evonav Settings → enable_icon_sync = 0 to bypass entirely.
"""

import frappe


def on_workspace_update(doc, method=None):
    """Sync evonav_workspace_icon → icon, then clear sidebar cache."""
    # Read Evonav Settings; bail if icon sync is disabled.
    try:
        settings = frappe.get_cached_doc("Evonav Settings")
    except frappe.DoesNotExistError:
        return
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Evonav icon sync: settings read failed")
        return

    if not settings.get("enable_icon_sync"):
        return

    custom_icon = (doc.get("evonav_workspace_icon") or "").strip()
    if not custom_icon:
        return  # Nothing to sync.

    # Only update if the standard icon differs — avoid recursive saves.
    if (doc.get("icon") or "").strip() == custom_icon:
        return

    # Update via db_set so we don't re-trigger on_update.
    doc.db_set("icon", custom_icon, update_modified=False)

    # Clear sidebar cache so the new icon renders on next desk load.
    # frappe.cache() (method) deprecated in v15+; fall back if needed.
    try:
        frappe.cache().delete_value("workspace_sidebar_items")
    except TypeError:
        frappe.cache.delete_value("workspace_sidebar_items")
    frappe.clear_cache(doctype="Workspace")
