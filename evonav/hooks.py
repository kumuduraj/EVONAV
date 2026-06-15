app_name = "evonav"
app_title = "Evonav"
app_publisher = "Evonet"
app_description = "Frappe Desk navbar/sidebar tweaks"
app_email = "admin@evonet.lk"
app_license = "MIT"

# ─────────────────────────────────────────────────────────────────────────────
# Static asset injection — the loader is small; the real payload is read from
# disk by boot.py and shipped inline via bootinfo. See Lesson #10 in the
# README for why we don't put the payload directly in app_include_js.
# ─────────────────────────────────────────────────────────────────────────────
app_include_js = [
    "/assets/evonav/js/evonav_loader.js",
]

app_include_css = [
    "/assets/evonav/css/navbar_hide.css",
]

# ─────────────────────────────────────────────────────────────────────────────
# Bootinfo extension — reads Evonav Settings and injects payload source +
# config into frappe.boot so the loader can pick it up client-side.
# ─────────────────────────────────────────────────────────────────────────────
extend_bootinfo = "evonav.boot.get_bootinfo"

# ─────────────────────────────────────────────────────────────────────────────
# Workspace icon sync — on every Workspace save, sync the custom icon field
# to the standard icon field and clear cache so the sidebar refreshes.
# ─────────────────────────────────────────────────────────────────────────────
doc_events = {
    "Workspace": {
        "on_update": "evonav.overrides.workspace_icon_sync.on_workspace_update",
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# Custom field for workspace icon — installed via fixtures.
# ─────────────────────────────────────────────────────────────────────────────
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            ["name", "in", ["Workspace-evonav_workspace_icon"]]
        ]
    }
]

# ─────────────────────────────────────────────────────────────────────────────
# Setup hooks — after install, create the default Evonav Settings Single
# with sensible defaults (About / Help / Frappe Support hidden).
# ─────────────────────────────────────────────────────────────────────────────
after_install = "evonav.install.after_install"
before_uninstall = "evonav.install.before_uninstall"
