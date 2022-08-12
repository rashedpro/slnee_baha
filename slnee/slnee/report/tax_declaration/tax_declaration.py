# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributo
# For license information, please see license.txt

import frappe
from frappe import _, scrub
from frappe.utils import add_days, add_to_date, flt, getdate
import calendar
from erpnext.accounts.utils import get_fiscal_year
from time import strptime

def execute(filters=None):
	if filters["type"] in ["Sales","المبيعات"]:
		filters["tree_type"]="Customer"
		filters["doc_type"]="Sales Invoice"
	else:
		filters["tree_type"]="Supplier"
		filters["doc_type"]="Purchase Invoice"
	filters["value_quantity"] = 'Value'
	filters["range"]="Monthly"
	#filters["from_date"]=d1
	#filters["to_date"]=d2
	return Analytics(filters).run()

class Analytics(object):
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or {})
		self.date_field = 'transaction_date'  if self.filters.doc_type in ['Sales Order', 'Purchase Order'] else 'posting_date'
		self.months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
		self.get_period_date_ranges()

	def run(self):
		self.get_columns()
		self.get_data()
		self.get_chart_data()
		# Skipping total row for tree-view reports
		skip_total_row = 0
		total_taxes=0
		total=0
		total_total=0
		for i in range(len(self.data)):
			total_taxes+=self.data[i]["taxes"]
			total+=self.data[i]["base_total"]
			total_total+=self.data[i]["taxes"]+self.data[i]["base_total"]
		if self.filters.tree_type in ["Supplier Group", "Item Group", "Customer Group", "Territory"]:
			skip_total_row = 1
		if self.filters["type"] in ["Sales","المبيعات"]:
			name=_("Total Buyers")
		else:
			name=_("Total Sellers")
		total_taxes=frappe.utils.fmt_money(total_taxes,currency="SAR")
		total=frappe.utils.fmt_money(total,currency="SAR")
		total_total=frappe.utils.fmt_money(total_total,currency="SAR")
		report_summary = [	{"label":name,"value":len(self.data),'indicator':'Blue',"width":50},
					 {"label":_("Total"),"value":"<span style='color:#8400f7;'>"+str(total)+"</span>",'indicator':'Orange',"width":50},
					{"label":_("Total Taxes"),"value":total_taxes,'indicator':'Red',"width":50},
					 {"label":_("Total included VAT"),"value":total_total,'indicator':'Green',"width":50}
]
		return self.columns, self.data ,None,None,report_summary



	def get_columns(self):

		self.columns = [{

				"label": _(self.filters.tree_type),

				"options": self.filters.tree_type if self.filters.tree_type != "Order Type" else "",

				"fieldname": "entity",

				"fieldtype": "Link" if self.filters.tree_type != "Order Type" else "Data",

				"width": 140 if self.filters.tree_type != "Order Type" else 200

			}]

		if self.filters.tree_type in ["Customer", "Supplier", "Item"]:

			self.columns.append({

				"label": _(self.filters.tree_type + " Name"),

				"fieldname": "entity_name",

				"fieldtype": "Data",

				"width": 280

			})



		if self.filters.tree_type == "Item":

			self.columns.append({

				"label": _("UOM"),

				"fieldname": 'stock_uom',

				"fieldtype": "Link",

				"options": "UOM",

				"width": 100

			})



		for i in range(1):

			if True :

				self.columns.append({

					"label": _("Base Total"),

					"fieldname": "base_total",

					"fieldtype": "Float",

					"width": 160

				})

				if self.filters["value_quantity"] == 'Value':

					self.columns.append({

        	                                "label": _("Taxes"),

                	                        "fieldname": "taxes",

                        	                "fieldtype": "Float",

                                	        "width": 120})

		if self.filters["value_quantity"] == 'Value':



			self.columns.append({

				"label": _("Grand Total"),

				"fieldname": "total",

				"fieldtype": "Float",

				"width": 160

		})



	def get_data(self):

		if self.filters.tree_type in ["Customer", "Supplier"]:

			self.get_sales_transactions_based_on_customers_or_suppliers()

			self.get_rows()



		elif self.filters.tree_type == 'Item':

			self.get_sales_transactions_based_on_items()

			self.get_rows()



		elif self.filters.tree_type in ["Customer Group", "Supplier Group", "Territory"]:

			self.get_sales_transactions_based_on_customer_or_territory_group()

			self.get_rows_by_group()



		elif self.filters.tree_type == 'Item Group':

			self.get_sales_transactions_based_on_item_group()

			self.get_rows_by_group()



		elif self.filters.tree_type == "Order Type":

			if self.filters.doc_type != "Sales Order":

				self.data = []

				return

			self.get_sales_transactions_based_on_order_type()

			self.get_rows_by_group()



		elif self.filters.tree_type == "Project":

			self.get_sales_transactions_based_on_project()

			self.get_rows()



	def get_sales_transactions_based_on_order_type(self):

		if self.filters["value_quantity"] == 'Value':

			value_field = "base_net_total"

		else:

			value_field = "total_qty"



		self.entries = frappe.db.sql(""" select s.order_type as entity, s.{value_field} as value_field, s.{date_field}

			from `tab{doctype}` s where s.docstatus = 1 and s.company = %s and s.{date_field} between %s and %s

			and ifnull(s.order_type, '') != '' order by s.order_type

		"""

		.format(date_field=self.date_field, value_field=value_field, doctype=self.filters.doc_type),

		(self.filters.company, self.filters.from_date, self.filters.to_date), as_dict=1)



		self.get_teams()



	def get_sales_transactions_based_on_customers_or_suppliers(self):

		if self.filters["value_quantity"] == 'Value':

			value_field = "base_net_total as value_field"

			v2="total_taxes_and_charges as taxes"

			v3="total_qty as qty"

		else:

			value_field = "total_qty as value_field"



		if self.filters.tree_type == 'Customer':

			entity = "customer as entity"

			entity_name = "customer_name as entity_name"

		else:

			entity = "supplier as entity"

			entity_name = "supplier_name as entity_name"

		if self.filters["value_quantity"] == 'Value':

			fields=[entity, entity_name, value_field,v2,v3, self.date_field]

		else:

			fields=[entity, entity_name, value_field, self.date_field]



		self.entries = frappe.get_all(self.filters.doc_type,

			fields=fields,

			filters={

				"docstatus": 1,

				"company": self.filters.company,

				self.date_field: ('between', [self.filters.from_date, self.filters.to_date])

			}

		)

		self.entity_names = {}

		for d in self.entries:

			self.entity_names.setdefault(d.entity, d.entity_name)



	def get_sales_transactions_based_on_items(self):



		if self.filters["value_quantity"] == 'Value':

			value_field = 'base_amount'

		else:

			value_field = 'stock_qty'



		self.entries = frappe.db.sql("""

			select i.item_code as entity, i.item_name as entity_name, i.stock_uom, i.{value_field} as value_field, s.{date_field}

			from `tab{doctype} Item` i , `tab{doctype}` s

			where s.name = i.parent and i.docstatus = 1 and s.company = %s

			and s.{date_field} between %s and %s

		"""

		.format(date_field=self.date_field, value_field=value_field, doctype=self.filters.doc_type),

		(self.filters.company, self.filters.from_date, self.filters.to_date), as_dict=1)



		self.entity_names = {}

		for d in self.entries:

			self.entity_names.setdefault(d.entity, d.entity_name)



	def get_sales_transactions_based_on_customer_or_territory_group(self):

		if self.filters["value_quantity"] == 'Value':

			value_field = "base_net_total as value_field"

		else:

			value_field = "total_qty as value_field"



		if self.filters.tree_type == 'Customer Group':

			entity_field = 'customer_group as entity'

		elif self.filters.tree_type == 'Supplier Group':

			entity_field = "supplier as entity"

			self.get_supplier_parent_child_map()

		else:

			entity_field = "territory as entity"



		self.entries = frappe.get_all(self.filters.doc_type,

			fields=[entity_field, value_field, self.date_field],

			filters={

				"docstatus": 1,

				"company": self.filters.company,

				self.date_field: ('between', [self.filters.from_date, self.filters.to_date])

			}

		)

		self.get_groups()



	def get_sales_transactions_based_on_item_group(self):

		if self.filters["value_quantity"] == 'Value':

			value_field = "base_amount"

		else:

			value_field = "qty"



		self.entries = frappe.db.sql("""

			select i.item_group as entity, i.{value_field} as value_field, s.{date_field}

			from `tab{doctype} Item` i , `tab{doctype}` s

			where s.name = i.parent and i.docstatus = 1 and s.company = %s

			and s.{date_field} between %s and %s

		""".format(date_field=self.date_field, value_field=value_field, doctype=self.filters.doc_type),

		(self.filters.company, self.filters.from_date, self.filters.to_date), as_dict=1)



		self.get_groups()



	def get_sales_transactions_based_on_project(self):

		if self.filters["value_quantity"] == 'Value':

			value_field = "base_net_total as value_field"

		else:

			value_field = "total_qty as value_field"



		entity = "project as entity"



		self.entries = frappe.get_all(self.filters.doc_type,

			fields=[entity, value_field, self.date_field],

			filters={

				"docstatus": 1,

				"company": self.filters.company,

				"project": ["!=", ""],

				self.date_field: ('between', [self.filters.from_date, self.filters.to_date])

			}

		)



	def get_rows(self):

		self.data = []

		self.get_periodic_data()

		

		for entity, period_data in self.entity_periodic_data.items():

			row = {

				"entity": entity,

				"entity_name": self.entity_names.get(entity) if hasattr(self, 'entity_names') else None

			}

			total = 0

			for i in range(1):

				if True :

					amount = flt(period_data.get("base_total", 0.0))

					row["base_total"] = amount

					row["taxes"]=period_data.get("taxes",0.0)

					total += amount+ row["taxes"]



			row["total"] = total



			if self.filters.tree_type == "Item":

				row["stock_uom"] = period_data.get("stock_uom")

			

			self.data.append(row)



	def get_rows_by_group(self):

		self.get_periodic_data()

		out = []



		for d in reversed(self.group_entries):

			row = {

				"entity": d.name,

				"indent": self.depth_map.get(d.name)

			}

			total = 0

			for end_date in self.periodic_daterange:

				period = self.get_period(end_date)

				amount = flt(self.entity_periodic_data.get(d.name, {}).get(period, 0.0))

				row[scrub(period)] = amount

				if d.parent and (self.filters.tree_type != "Order Type" or d.parent == "Order Types"):

					self.entity_periodic_data.setdefault(d.parent, frappe._dict()).setdefault(period, 0.0)

					self.entity_periodic_data[d.parent][period] += amount

				total += amount



			row["total"] = total

			out = [row] + out



		self.data = out



	def get_periodic_data(self):

		self.entity_periodic_data = frappe._dict()

		for d in self.entries:

			if self.filters.tree_type == "Supplier Group":

				d.entity = self.parent_child_map.get(d.entity)

			if True :

				self.entity_periodic_data.setdefault(d.entity, frappe._dict()).setdefault("base_total", 0.0)

				self.entity_periodic_data.setdefault(d.entity, frappe._dict()).setdefault("taxes", 0.0)

				self.entity_periodic_data[d.entity]["base_total"] += flt(d.value_field)

				self.entity_periodic_data[d.entity]["taxes"] += flt(d.taxes)

				if self.filters.tree_type == "Item":

					self.entity_periodic_data[d.entity]['stock_uom'] = d.stock_uom



	def get_period(self, posting_date):

		if self.filters.range == 'Weekly':

			period = "Week " + str(posting_date.isocalendar()[1]) + " " + str(posting_date.year)

		elif self.filters.range == 'Monthly':

			period = str(self.months[posting_date.month - 1]) + " " + str(posting_date.year)

		elif self.filters.range == 'Quarterly':

			period = "Quarter " + str(((posting_date.month - 1) // 3) + 1) + " " + str(posting_date.year)

		else:

			year = get_fiscal_year(posting_date, company=self.filters.company)

			period = str(year[0])

		return period



	def get_period_date_ranges(self):

		from dateutil.relativedelta import MO, relativedelta

		from_date, to_date = getdate(self.filters.from_date), getdate(self.filters.to_date)



		increment = {

			"Monthly": 1,

			"Quarterly": 3,

			"Half-Yearly": 6,

			"Yearly": 12

		}.get(self.filters.range, 1)



		if self.filters.range in ['Monthly', 'Quarterly']:

			from_date = from_date.replace(day=1)

		elif self.filters.range == "Yearly":

			from_date = get_fiscal_year(from_date)[1]

		else:

			from_date = from_date + relativedelta(from_date, weekday=MO(-1))



		self.periodic_daterange = []

		for dummy in range(1, 53):

			if self.filters.range == "Weekly":

				period_end_date = add_days(from_date, 6)

			else:

				period_end_date = add_to_date(from_date, months=increment, days=-1)



			if period_end_date > to_date:

				period_end_date = to_date



			self.periodic_daterange.append(period_end_date)



			from_date = add_days(period_end_date, 1)

			if period_end_date == to_date:

				break



	def get_groups(self):

		if self.filters.tree_type == "Territory":

			parent = 'parent_territory'

		if self.filters.tree_type == "Customer Group":

			parent = 'parent_customer_group'

		if self.filters.tree_type == "Item Group":

			parent = 'parent_item_group'

		if self.filters.tree_type == "Supplier Group":

			parent = 'parent_supplier_group'



		self.depth_map = frappe._dict()



		self.group_entries = frappe.db.sql("""select name, lft, rgt , {parent} as parent

			from `tab{tree}` order by lft"""

		.format(tree=self.filters.tree_type, parent=parent), as_dict=1)



		for d in self.group_entries:

			if d.parent:

				self.depth_map.setdefault(d.name, self.depth_map.get(d.parent) + 1)

			else:

				self.depth_map.setdefault(d.name, 0)



	def get_teams(self):

		self.depth_map = frappe._dict()



		self.group_entries = frappe.db.sql(""" select * from (select "Order Types" as name, 0 as lft,

			2 as rgt, '' as parent union select distinct order_type as name, 1 as lft, 1 as rgt, "Order Types" as parent

			from `tab{doctype}` where ifnull(order_type, '') != '') as b order by lft, name

		"""

		.format(doctype=self.filters.doc_type), as_dict=1)



		for d in self.group_entries:

			if d.parent:

				self.depth_map.setdefault(d.name, self.depth_map.get(d.parent) + 1)

			else:

				self.depth_map.setdefault(d.name, 0)



	def get_supplier_parent_child_map(self):

		self.parent_child_map = frappe._dict(frappe.db.sql(""" select name, supplier_group from `tabSupplier`"""))



	def get_chart_data(self):

		length = len(self.columns)



		if self.filters.tree_type in ["Customer", "Supplier"]:

			labels = [d.get("label") for d in self.columns[2:length - 1]]

		elif self.filters.tree_type == "Item":

			labels = [d.get("label") for d in self.columns[3:length - 1]]

		else:

			labels = [d.get("label") for d in self.columns[1:length - 1]]

		self.chart = {

			"data": {

				'labels': labels,

				'datasets': []

			},

			"type": "line"

		}
