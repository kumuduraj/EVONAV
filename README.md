# evonav

Frappe Desk tweaks for workspace icons and navbar items.

## Features

1. **Workspace icon sync** — adds a custom field `evonav_workspace_icon` to
   Workspace. On save, the icon is synced to the standard `icon` field and
   sidebar cache is cleared, so the icon renders immediately.

2. **Navbar hide** — hides navbar items by label. Default hidden labels:
   "About", "Help", "Frappe Support". Configurable via the `Evonav Settings`
   Single DocType.

## Configuration

After install, visit `/app/evonav-settings` to toggle features and
configure the navbar hide list.

## License

MIT
