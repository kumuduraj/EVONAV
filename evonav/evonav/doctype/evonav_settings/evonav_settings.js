frappe.ui.form.on("Evonav Settings", {
    refresh(frm) {
        frm.add_custom_button(__("How this works"), () => {
            frappe.msgprint({
                title: __("Evonav — How this works"),
                indicator: "blue",
                message: `
                    <p><b>Workspace Icon Sync</b><br>
                    Adds a "Evonav Workspace Icon" field to every Workspace.
                    On save, that value is synced to the standard icon field
                    and the sidebar cache is cleared so the icon renders
                    immediately.</p>

                    <p><b>Navbar Hide</b><br>
                    Hides navbar items by label match. Configure one label
                    per line in the "Navbar Hide Labels" field. Matching is
                    case-insensitive.</p>

                    <p><b>Defaults installed:</b> About, Help, Frappe Support.</p>

                    <p>Changes take effect on the next page load (no bench
                    restart needed).</p>
                `,
            });
        });
    },
});
