import frappe


@frappe.whitelist()
def test():
	print(100*"5")
