# Copyright (c) 2022, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from slnee.slnee.doctype.wordpress_store.wordpress_store import get_api

from frappe.model.document import Document

class StoreCategory(Document):
	
	def after_rename(self):
		frappe.msgprint("renamed")


	def after_insert(self):
		if  not frappe.get_doc("Wordpress Store").sync:
			return
		if not self.update_store:
			self.update_store=1
			self.save()
			frappe.db.commit()
			return
		site_url="https://business.zerabi.deom.com.sa"
		data={"name":self.name}
		desc=self.description or ''
		data["description"]=desc
		if self.image:
			data["image"]={"src":site_url+self.image}
		wcapi=get_api(timeout=15)
		if wcapi ==-1:
			frappe.throw("Failed o connect To server.")
		r=wcapi.post("products/categories",data=data).json()
		try:
			self.id=r["id"]
			self.save()
			frappe.db.commit()
		except:
			pass
		return

	def before_save(self):
		if not frappe.get_doc("Wordpress Store").sync:
			return
		if not self.update_store:
			return
		data={"name":self.name}
		desc=self.description or ''
		data["description"]=desc
		url="products/categories/"+str(self.id)
		if self.image:
			site_url="https://business.zerabi.deom.com.sa"
			data["image"]={"src":site_url+self.image}
		try:
			wcapi=get_api(timeout=10)
			r=wcapi.put(url,data).json()
		except:
			return

	def after_delete(self):
		if not frappe.get_doc("Wordpress Store").sync:
			return
		try:
			wcapi=get_api(timeout=10)
			url="products/categories/"+str(self.id)
			r=wcapi.delete(url, params={"force": True})
		except:
			pass
