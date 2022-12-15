# Copyright (c) 2022, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AddItemstoStoreTool(Document):
	@frappe.whitelist()
	def insert_items(self):
		if self.category_type=="Create new category":
			category_name=self.new_category
			if not category_name:
				return
			doc=frappe.new_doc("Store Category")
			doc.name1=category_name
			doc.update_store=1
			item_group=frappe.get_doc("Item Group",self.item_group)
			if item_group.image:
				doc.image=item_group.image
			if not frappe.db.exists("Store Category",category_name):
				doc.insert(ignore_if_duplicate=True)
				frappe.db.commit()
		else:
			category_name=self.old_category
			if not category_name:
				return
		for i in self.items:
			item=frappe.get_doc("Item",i.item)
			doc = frappe.new_doc('Store Item')
			doc.update_store=1
			doc.name1=i.item
			doc.warehouse=self.warehouse
			doc.type="simple"
			doc.status=self.status
			doc.items=[i]
			doc.manage_stock=1
			doc.stock_quantity=i.stock
			doc.sale_price=i.sale_price
			doc.on_sale=1 if doc.sale_price >0 else 0
			tax=i.price*0.15
			doc.tax=tax
			doc.desxription=item.description if item.description else ""

			doc.regular_price=i.price+tax
			doc.image_1 = item.image if item.image else ""
			category=doc.append("categories",{})
			category.category=category_name
			doc.insert()
			frappe.db.commit()


	@frappe.whitelist()
	def set_defaults(self):
		settings=frappe.get_doc("Wordpress Store")
		self.warehouse=settings.default_warehouse or ""
		self.price_list=settings.price_list or ""
		self.tax_template=settings.sales_taxes_and_charges_template or ""


	@frappe.whitelist()
	def get_items(self,item_group):
		items=frappe.db.get_list("Item",filters={"item_group":item_group})
		self.items=[]
		have_price=self.have_price_list
		in_stock=self.in_stock
		n=0
		for i in items:
			price=0
			stock=0
			rates=frappe.db.get_list("Item Price",filters={"item_code":i.name,"price_list":self.price_list},fields=["price_list_rate"],order_by="valid_from desc")
			if len(rates)>0:
				price=rates[0]["price_list_rate"]
			bins=frappe.db.get_list("Bin",filters={"item_code":i.name,"warehouse":self.warehouse},fields=["actual_qty"])
			if len(bins)>0:
					stock=bins[0]["actual_qty"]
			if (price or not have_price)  and (stock or not in_stock):
				add=self.append("items",{})
				add.price=price
				add.stock=stock
				add.item=i["name"]
				n+=1
		self.items_number=n
