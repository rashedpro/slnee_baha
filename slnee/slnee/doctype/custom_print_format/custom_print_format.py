# Copyright (c) 2021, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CustomPrintFormat(Document):
	def validate(self):
		if not frappe.db.exists(doc.doc_type,doc.name):
			doc = frappe.get_doc({
				'doctype':'Print Format',
				"name":doc.name,
				'doc_type':self.doc_type,
				"disabled":self.disabled,
				"html":self.demo,
				"Standard": "No",
				"custom_format":1,
				"print_format_type":"Jinja"}).insert()

	pass
