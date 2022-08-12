# Copyright (c) 2022, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from woocommerce import API
from frappe.model.document import Document

class WordpressStore(Document):
	@frappe.whitelist()
	def test(self):
		if not self.url:
			return _("Url is missing")
		if not self.key:
			return _("Key is missing")
		if not self.secret:
			return _("Secret is missing")
		try:
			wcapi=API(url=self.url,consumer_key=self.key,consumer_secret=self.secret,version="wc/v3")
		except :
			return ("Failed To connect to server!")
		r = wcapi.get("orders")
		if r.status_code==200:
			return ("Connected to server.")
		elif r.status_code ==403:
			return ("Error 403, You don't have permission to access this resource.")
		return str(r.status_code)


	@frappe.whitelist()
	def get_categories(self):
		wcapi=self.get_api()
		if wcapi==-1:
			return
		categories=wcapi.get("products/categories")
		for c in categories.json():
			doc=frappe.new_doc('Store Category')
			doc.name1=c["name"]
			doc.id=c["id"]
			doc.description=c["description"]
			try:
				doc.image=c["image"]["src"]
			except:
				pass
			doc.insert()
		frappe.db.commit()
	@frappe.whitelist()
	def get_products(self):
		wcapi=self.get_api()
		if wcapi==-1:
			return
		products=wcapi.get("products",params={"per_page":100})
		for p in products.json():
			doc=frappe.new_doc("Store Item")
			doc.id=p["id"]
			doc.name1=p["name"]
			doc.type=p["type"]
			doc.description=p["description"]
			doc.short_description=p["short_description"]
			doc.on_sale = 1 if p["on_sale"] else 0
			doc.permalink=p["permalink"]
			doc.regular_price=float(p["regular_price"])
			doc.insert()

	def get_api(self):
		try:
			wcapi=API(url=self.url,consumer_key=self.key,consumer_secret=self.secret,version="wc/v3")
			return wcapi
		except:
			return -1
