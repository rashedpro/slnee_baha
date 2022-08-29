# Copyright (c) 2022, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from slnee.slnee.doctype.wordpress_store.wordpress_store import get_api
class StoreItem(Document):
	not_saved=_("Item Not saved to store!")
	saved=_("Item updated in the store.")
	def after_insert(self):
		if not frappe.get_doc("Wordpress Store").sync:
			return
		if not self.update_store:
			self.update_store=1
			self.save()
			frappe.db.commit()
			return
		datas=self.get_data()
		#frappe.throw(str(datas))
		wcapi=get_api(timeout=15)
		if wcapi ==-1:
			frappe.throw("Failed o connect To server.")
		r=wcapi.post("products",data=datas).json()
		try:
			self.id=r["id"]
			self.permalink=r["permalink"]
			self.save()
			frappe.db.commit()
		except:
			pass
		return

	def before_save(self):
		if not frappe.get_doc("Wordpress Store").sync:
			return
		if not self.id or not self.update_store:
			return
		url="products/"+str(self.id)
		data=self.get_data()
		try:
			wcapi=get_api(timeout=10)
			r=wcapi.put(url,data).json()
			#frappe.msgprint(self.saved,raise_exception=False)
		except:
			#frappe.msgprint(self.not_saved,raise_exception=False)
			return

	def get_data(self):
		site_url="https://business.zerabi.deom.com.sa"
		data={"name":self.name,"type":self.type,"status":self.status,"regular_price":str(self.regular_price),"sale_price":"","description":self.description,"short_description":self.short_description,"weight":str(self.weight)}
		if self.on_sale:
			data["sale_price"]=str(self.sale_price)
		if self.manage_stock:
			data["manage_stock"]=True
			data["stock_quantity"]=str(self.stock_quantity)
			if "but" in self.backorders:
				data["backorders"]="notify"
			else:
				data["backorders"]=str(self.backorders).lower()
		else:
			data["manage_stock"]=False
		length = self.length or 0
		width=self.width or 0
		height=self.height or 0
		dimensions={"length":str(self.length),"width":str(self.width),"height":str(self.height)}
		data["dimensions"]=dimensions
		self_dict=self.__dict__
		images=[]
		for i in range(1,6):
			if self_dict['image_'+str(i)]:
				if 'http' not in self_dict["image_"+str(i)]:
					images.append({"src":site_url+self_dict["image_"+str(i)]})
				else:
					images.append({"src":self_dict["image_"+str(i)]})
		data["images"]=images
		return data

@frappe.whitelist()
def get_item_info(item,warehouse=None):
	if True:
		settings=frappe.get_doc("Wordpress Store")
		list=frappe.db.get_list('Item Price',filters={"item_code":item,"price_list":settings.price_list,"selling":1},order_by="valid_from desc")
		price=0
		if len(list)>0:
			price=frappe.get_doc("Item Price",list[0]["name"]).price_list_rate
		if not warehouse:
			warehouse=settings.default_warehouse
		bins=frappe.db.get_list("Bin",filters={"warehouse":warehouse,"item_code":item})
		stock=0
		if len(bins)>0:
			stock=frappe.db.get_value("Bin",bins[0]["name"],"projected_qty")
			stock = 0 if stock <0 else stock
		tax_per = settings.tax_per or 0
		tax=tax_per*price
		return ("{}#{}#{}").format(price,stock,tax)
@frappe.whitelist()
def get_tax_per():
	settings=frappe.get_doc("Wordpress Store")
	tax_per = settings.tax_per or 0
	return tax_per
