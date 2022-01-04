# Copyright (c) 2021, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CustomPrintFormat(Document):
	def validate(self):
		if frappe.db.exists("Print Format",self.name) ==None:
			html=""
			css= self.css if self.css else ""
			if self.links:
				html+=self.links
			if self.html:
				html+=self.html
			doc = frappe.get_doc({
				'doctype':'Print Format',
				"name":self.name,
				'doc_type':self.doc_type,
				"disabled":self.is_disabled,
				"html":html,
				"css":css,
				"Standard": "No",
				"custom_format":1,
				"print_format_type":"Jinja"}).insert(ignore_if_duplicate=True)
		else:
			doc=frappe.get_doc("Print Format",self.name)
			html=""
			css= self.css if self.css else ""
			if self.links:
				tml+=self.links
			if self.html:
				html+=self.html
			doc.html=html
			doc.css=css
			doc.disabled=self.is_disabled
			doc.save()
	pass
