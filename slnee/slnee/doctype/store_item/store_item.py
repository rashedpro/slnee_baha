# Copyright (c) 2022, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StoreItem(Document):


	def before_save(self):
		pass

	def get_data(self):
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
		return
		dimensions={"length":str(self.length),"width":str(self.width),"height":str(self.height)}
		data["dimensions"]=dimensions
		return data
