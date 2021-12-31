# Copyright (c) 2021, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CustomPrintFormat(Document):
	def validate(self):
		if frappe.db.exists("Print Format",self.name) ==None:
			print(100*"7")
			doc = frappe.get_doc({
				'doctype':'Print Format',
				"name":self.name,
				'doc_type':self.doc_type,
				"disabled":self.is_disabled,
				"html":self.links+self.html,
				"css":self.css,
				"Standard": "No",
				"custom_format":1,
				"print_format_type":"Jinja"}).insert(ignore_if_duplicate=True)

	pass
