# Copyright (c) 2022, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from slnee.slnee.doctype.wordpress_store.wordpress_store import get_api
class StoreItem(Document):
	not_saved=_("Item Not saved to store!")
	saved=_("Item updated in the store.")

	#def before_rename(self):
	#	frappe.throw("before")

	def after_rename(self,old,new,merge):
		self.sync_name(show_alert=True)


	def validate(self):
		if self.type=="variable":
			if not self.attribute:
				frappe.throw("Attribute is missing")
			if len(self.items)==0:
				frappe.throw("Items table is empty!")
			terms=[i.term for i in self.items]
			#frappe.throw(str(terms))
			for i in range(len(terms)):
				if not terms[i]:
					frappe.throw("Variant is missing in table items line {}.".format(i+1))
				indices = [o for o, x in enumerate(terms) if x == terms[i]]
				#frappe.throw(str(indices))
				if len(indices)>1:
					frappe.throw("Variant {} is duplicated in line {} and {}.".format(terms[i],indices[0]+1,indices[1]+1))
			#frappe.throw(str(terms))
			#first=self.items[0].item
			#for i in self.items:
			#	if i.item!=first:
			#		frappe.throw("Product has variants. All Items should be the same!")
		warehouses=self.warehouse
		type="local"
		if len(warehouses)==0:
			warehouses=frappe.get_doc("Wordpress Store").default_warehouse
			type="default"
		if len(warehouses)==0:
			type="all"
		warehouses=str([w.warehouse for w in warehouses])
		#frappe.throw(warehouses)
		self.warehouse_type=type
		for i in self.items:
			i.warehouse=warehouses
			i.warehouse_type=type
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
			frappe.msgprint("saved to store")
		except:
			pass
		return

	def after_delete(self):
		if not frappe.get_doc("Wordpress Store").sync:
			return
		url="products/"+str(self.id)
		try:
			wcapi=get_api(timeout=15)
			r=wcapi.delete(url, params={"force": True}).json()
		except:
			pass

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

	@frappe.whitelist()
	def sync_name(self,show_alert=False):
		if not self.id:
			return
		data={"name":self.name}
		wcapi=get_api(timeout=15)
		url="products/"+str(self.id)
		try:
			r=wcapi.put(url,data).json()
			if show_alert:
				frappe.msgprint(
					_("document name was synced to the shop  successfully."),
					alert=True,
					indicator="green",
				)
		except:
			return

	@frappe.whitelist()
	def sync_stock(self):
		if not self.id:
			return
		data={"stock_quantity":str(self.stock_quantity)}
		wcapi=get_api(timeout=15)
		url="products/"+str(self.id)
		try:
			r=wcapi.put(url,data).json()
		except:
			return

	@frappe.whitelist()
	def sync_to_store(self,show_alert=False):
		if self.type=="variable":
			if not self.attribute:
				frappe.throw("Atribute is missing")
			l=1
			for i in self.items:
				if not i.term:
					frappe.throw("Term is missing in line {}".format(l))
				l+=1
		if not self.id :
			datas=self.get_data()
			wcapi=get_api(timeout=15)
			if wcapi ==-1:
				frappe.throw("Failed o connect To server.")
			r=wcapi.post("products",data=datas).json()
			#frappe.throw(str(r))
			if True:
				self.id=r["id"]
				self.permalink=r["permalink"]
				self.save()
				frappe.db.commit()
				if show_alert:
					frappe.msgprint(_("Item inserted to the Shop."),alert=True,indicator="green")
			else:
				frappe.throw("Unknown error")

		else:
			url="products/"+str(self.id)
			data=self.get_data()
			if True:
				wcapi=get_api(timeout=10)
				r=wcapi.put(url,data).json()
				if show_alert:
					frappe.msgprint(_("Item synced with the shop."),alert=True,indicator="green")
				#frappe.throw(self.type)
		url="products/"+str(self.id)
		if True:
			if True:
				if self.type=="variable":
					#frappe.throw("variable")
					#options=data["attributes"]["options"]
					update=[]
					create=[]
					ids=""
					old_ids=[]
					if self.variants:
						old_ids=self.variants.split("#")
					
					new_ids=[str(i.id) for i in self.items]
					delete=[]
					if len(old_ids) >0 and old_ids[-1]=="":
						old_ids.pop(-1)
					for d in old_ids:
						if d not in new_ids:
							delete.append(d)
					re={"delete":delete}
					for i in self.items:
						d={"regular_price":str(i.price*1.15),"stock_quantity":str(i.stock),"attributes":[{"name":self.attribute,"option":i.term}]}


						if i.image:
							site_url="https://business.zerabi.deom.com.sa"
							d["image"]={"src":site_url+i.image}
						if i.sale_price:
							d["sale_price"]=str(i.sale_price)
						#frappe.throw(str(d))
						if not i.id:
							create.append(d)
							r=wcapi.post(url+"/variations", d).json()
							#frappe.throw(str(r))
							i.id=r["id"]
							ids+=str(r["id"])+"#"
						else:
							d["id"]=i.id
							update.append(d)
							ids+=str(i.id)+"#"
							#r=wcapi.put(url+"/variations/"+str(i.id),d).json()
						#frappe.throw(str(r))
					re["update"]=update
					#frappe.throw(str(re))
					r=wcapi.post(url+"/variations/batch",re).json()
					if show_alert:
						frappe.msgprint(_("Variants updated for item {}.".format(self.name)),alert=True,indicator="green")
					self.variants=ids
					self.last_sync=frappe.utils.get_datetime()
					self.save()
					frappe.db.commit()
			else:
				frappe.throw("Unknown error")
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
		categories=[]
		for c in self.categories:
			id=frappe.get_doc("Store Category",c.category).id
			categories.append({"id":id})
		data["categories"]=categories
		for i in range(1,6):
			if self_dict['image_'+str(i)]:
				if 'http' not in self_dict["image_"+str(i)]:
					images.append({"src":site_url+self_dict["image_"+str(i)]})
				else:
					images.append({"src":self_dict["image_"+str(i)]})
		data["images"]=images
		if self.type=="variable":
			attribute={"name":self.attribute,"variation":True,"visible":True}
			options=[]
			for i in self.items:
				options.append(i.term)
			attribute["options"]=options
			data["attributes"]=[attribute]
			#data["menu_order"]="1"
		return data

@frappe.whitelist()
def get_item_info(item,warehouse=None):
	#frappe.throw(warehouse[0])
	if True:
		settings=frappe.get_doc("Wordpress Store")
		list=frappe.db.get_list('Item Price',filters={"item_code":item,"price_list":settings.price_list,"selling":1},order_by="valid_from desc")
		price=0
		if len(list)>0:
			price=frappe.get_doc("Item Price",list[0]["name"]).price_list_rate
		warehouse=warehouse.replace("[","").replace("]","").split(",")
		warehouse=[i[1:-1] for i in warehouse]
		#frappe.throw(str(warehouse))
		if not warehouse or warehouse=="[]" or warehouse =="['']" or warehouse==['']:
			warehouse=settings.default_warehouse
			warehouse=[b.warehouse for b in warehouse]
		#frappe.throw(str(warehouse))
		if not warehouse:
			filters={"item_code":item}
		else:
			#warehouses=[]
			#for w in warehouse:
				#warehouses.append(w)
			#frappe.throw(str(warehouse))
			filters=[["warehouse","in",warehouse],['item_code',"in",[item]]]
		bins=frappe.db.get_list("Bin",filters=filters,fields=["name","projected_qty"])
		stock=0
		for b in bins:
			stock+=b["projected_qty"]
		stock = 0 if stock <0 else stock
		tax_per = settings.tax_per or 0
		tax=tax_per*price
		return ("{}#{}#{}").format(price,stock,tax)
@frappe.whitelist()
def get_tax_per():
	settings=frappe.get_doc("Wordpress Store")
	tax_per = settings.tax_per or 0
	return tax_per
