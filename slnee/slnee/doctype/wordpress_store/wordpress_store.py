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
	def get_orders(self):
		wcapi=get_api(timeout=10)
		settings=frappe.get_doc("Wordpress Store")
		if wcapi==-1:
			return
		orders=wcapi.get("orders",params={"per_page":100})
		for o in orders.json()[:10]:
			customer_id=o["customer_id"]
			#frappe.throw(str(o["customer_id"]))
			l=frappe.db.get_list("Customer",filters={"wordpress_id":customer_id})
			if len(l)==0:
				name=get_customer(customer_id)
			else:
				name=l[0]["name"]
			if not name:
				return
			doc=frappe.new_doc("Quotation")
			doc.naming_series=settings.quotations_series
			doc.order_type="Shopping_cart"
			doc.party_name=name
			frappe.throw("here")
			for i in o["line_items"]:
				item=frappe.get_doc("Store Item",i["name"])
				qty=i["quantity"]
				for it in item.items:
					row=doc.append("items", {})
					row.item_code=it.item
					row.qty=qty
					if it.sale_price and it.sale_price < it.price:
						row.rate=it.sale_price
					else:
						row.rate=it.price
			doc.insert()
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
			doc.insert(ignore_if_duplicate=True)
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
			doc.update_store=0
			doc.name1=p["name"]
			doc.type=p["type"]
			doc.status=p["status"]
			doc.description=p["description"]
			doc.short_description=p["short_description"]
			doc.on_sale = 1 if p["on_sale"] else 0
			doc.permalink=p["permalink"]
			try:
				doc.regular_price=float(p["regular_price"])
			except:
				doc.regular_price=0
			if p["sale_price"]!="":
				doc.sale_price=float(p["sale_price"])
			doc.manage_stock=1 if p["manage_stock"] else 0
			if doc.manage_stock:
				try:
					doc.stock_quantity=p["stock_quantity"]
				except:
					doc.stock_quantity=0
				if p["backorders"]=="no":
					doc.backorders="No"
				elif p["backorders"]=="yes":
					doc.backorders="Yes"
				else:
					doc.backorders="Yes, but with customer notification"
			n=1
			for i in p["images"]:
				if n==1:
					doc.image_1=i["src"]
				if n==2:
					doc.image_2=i["src"]
				if n==3:
					doc.image_3=i["src"]
				if n==4:
					doc.image_4=i["src"]
				if n==5:
					doc.image_5=i["src"]
				if n==6:
					doc.image_6=i["src"]
				n+=1
			for e in p["related_ids"]:
				item= doc.append("related_ids",{})
				item.id=e
			doc.insert(ignore_if_duplicate=True)
		return 
	@frappe.whitelist()
	def get_customers(self):
		wcapi=self.get_api()
		if wcapi==-1:
			return
		customers=wcapi.get("customers",params={"per_page":100})
		settings=frappe.get_doc("Wordpress Store")
		if not settings.customer_group or not settings.territory :
			return
		for c in customers.json():
			n=save_customer(c,settings)
			name = c["first_name"]+" "+c["last_name"]
			if name  not in [""," ",None]:
				break
	@frappe.whitelist()
	def get_taxes(self):
		self.taxes=[]
		self.tax_per=0
		if self.sales_taxes_and_charges_template:
			taxes=frappe.get_doc("Sales Taxes and Charges Template",self.sales_taxes_and_charges_template).taxes
			self.taxes=taxes
			self.tax_per=taxes[0].rate/100
	def get_api(self):
		try:
			wcapi=API(url=self.url,consumer_key=self.key,consumer_secret=self.secret,version="wc/v3")
			return wcapi
		except:
			return -1
def get_customer(id):
	wcapi=get_api()
	if wcapi==-1:
		return
	url="customers/"+str(id)
	c=wcapi.get(url).json()
	#settings=frappe.get_doc("Wordpress Store")
	if "id" in c.keys():
		settings=frappe.get_doc("Wordpress Store")
		return save_customer(c,settings)
	return
def save_customer(c,settings):
	if True:
		doc=frappe.new_doc("Customer")
		doc.customer_group=settings.customer_group
		doc.territory=settings.territory
		doc.wordpress_id=c["id"]
		doc.customer_name=c["first_name"]+" "+c["last_name"]
		try:
			doc.mobile_no=c["billing"]["phone"]
		except:
			a=0
		if doc.customer_name not in [""," ",None]:
			doc.insert(ignore_if_duplicate=True)
			if c["billing"]:
				bill=c["billing"]
				address=frappe.new_doc("Address")
				address.address_title=doc.name
				address.address_line1=bill["address_1"]
				address.address_line2=bill["address_2"]
				address.city=bill["city"]
				if not address.city:
					address.city="Saudi Arabia"
				address.state=bill["state"]
				address.pincode=bill["postcode"]
				address.phone=bill["phone"]
				address.email=c["email"]
				customer=address.append("links",{})
				customer.link_doctype="Customer"
				customer.link_name=doc.name
				address.insert()
			return doc.name
		return
def get_api(timeout=5):
	doc=frappe.get_doc("Wordpress Store")
	try:
		wcapi=API(url=doc.url,consumer_key=doc.key,consumer_secret=doc.secret,timeout=timeout)
		return wcapi
	except:
		return -1
