# Copyright (c) 2022, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import json
import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.stock.get_item_details import get_default_bom
from frappe.utils import add_days, cint, cstr, flt, get_link_to_form, getdate, nowdate, strip_html


class InternSalesOrder(Document):

	def on_submit(self):
		self.status='Open'

	def on_cancel(self):
		self.status="Cancelled"


	@frappe.whitelist()
	def get_work_order_items(self, for_raw_material_request=0):
		"""Returns items with BOM that already do not have a linked work order"""
		items = []
		item_codes = [i.item_code for i in self.items]
		product_bundle_parents = [
			pb.new_item_code
			for pb in frappe.get_all(
				"Product Bundle", {"new_item_code": ["in", item_codes]}, ["new_item_code"]
			)
		]

		for table in [self.items]:
			for i in table:
				bom = get_default_bom(i.item_code)
				stock_qty = i.qty 

				if not for_raw_material_request:
					total_work_order_qty = flt(
						frappe.db.sql(
							"""select sum(qty) from `tabWork Order`
						where production_item=%s and sales_order=%s and sales_order_item = %s and docstatus<2""",
							(i.item_code, self.name, i.name),
						)[0][0]
					)
					pending_qty = stock_qty - total_work_order_qty
				else:
					pending_qty = stock_qty

				if pending_qty and i.item_code not in product_bundle_parents:
					items.append(
						dict(
							name=i.name,
							item_code=i.item_code,
							description=i.description,
							bom=bom or "",
							warehouse=i.warehouse,
							pending_qty=pending_qty,
							required_qty=pending_qty if for_raw_material_request else 0,
							sales_order_item=i.name,
						)
					)

		return items
@frappe.whitelist()
def make_work_orders(items, sales_order, company, project=None):
	"""Make Work Orders against the given Sales Order for the given `items`"""
	items = json.loads(items).get("items")
	out = []

	for i in items:
		if not i.get("bom"):
			frappe.throw(_("Please select BOM against item {0}").format(i.get("item_code")))
		if not i.get("pending_qty"):
			frappe.throw(_("Please select Qty against item {0}").format(i.get("item_code")))

		work_order = frappe.get_doc(
			dict(
				doctype="Work Order",
				production_item=i["item_code"],
				bom_no=i.get("bom"),
				qty=i["pending_qty"],
				company=company,
				inter_sales_order=sales_order,
				#sales_order_item=i["sales_order_item"],
				project=project,
				fg_warehouse=i["warehouse"],
				description=i["description"],
			)
		).insert()
		work_order.set_work_order_operations()
		work_order.flags.ignore_mandatory = True
		work_order.save()
		out.append(work_order)

	frappe.db.set_value("Intern Sales Order",sales_order,"status","Manufactured")
	return [p.name for p in out]
