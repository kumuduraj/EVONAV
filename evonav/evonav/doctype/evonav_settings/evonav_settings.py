import frappe
from frappe.model.document import Document


class EvonavSettings(Document):
    def validate(self):
        # Normalize line endings and strip blank lines.
        if self.navbar_hide_labels:
            lines = [
                line.strip()
                for line in self.navbar_hide_labels.splitlines()
                if line.strip()
            ]
            self.navbar_hide_labels = "\n".join(lines)

    def on_update(self):
        # Clear cached bootinfo so changes take effect on next page load
        # without a bench restart.
        frappe.clear_cache()
