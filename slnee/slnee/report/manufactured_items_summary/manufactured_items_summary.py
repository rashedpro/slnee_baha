# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from collections import defaultdict

import frappe
from frappe import _
from frappe.utils import date_diff, flt, getdate, today

from erpnext.stock.report.stock_analytics.stock_analytics import get_period, get_period_date_ranges


def execute(filters=None):
	columns, data = [], []
	filters["chart_based_on"]="items"
	if not filters.get("age"):
		filters["age"] = 0
	dataa=get_data(filters)
	data = dataa["res"]
	columns = get_columns(filters)
	#chart_data = get_chart_data(data, filters)
	link="a"
	cards=[
		{"label":_("Total Items"),"value":dataa["total_items"],'indicator':'Blue',"width":50},
		{"label":_("Total Produced Quantity"),"value":dataa["total_produced_qty"],'indicator':'Green',"width":50},
	]
	if not link and filters["status"] =="Completed":
		cards.append({"label":_("Max Produced Quantity"),"value":str(dataa["max_name"])+"("+str(dataa["max_produced_qty"])+")",'indicator':'Red',"width":50})
	if link and filters["status"] == "Completed":
		cards.append({"label":_("Max Produced Quantity"),"value":"<a href='"+link+"/app/item/{}' style='color:#4de3fa !important;'>{}</a>".format(dataa["max_name"],dataa["max_name"])+"("+str(dataa["max_produced_qty"])+")",'indicator':'Red',"width":50})
	if filters["status"]=="Completed":
		cards.append({"label":_("Today Produced Quantity"),"value":dataa["total_today"],'indicator':'Green',"width":50})
	if filters["status"] in [ "Not Started" , "In Process"]:
		cards.insert(1,{"label":_("Total Quantity To Produce"),"value":dataa["total_qty"],'indicator':'Pink',"width":50})
	chart=dataa["chart"]
	return columns, data, None, chart,cards


def get_data(filters):
	query_filters = {"docstatus": ("<", 2)}

	fields = [
		"name",
		"status",
		"sales_order",
		"production_item",
		"qty",
		"produced_qty",
		"planned_start_date",
		"planned_end_date",
		"actual_start_date",
		"actual_end_date",
		"lead_time",
	]

	for field in ["sales_order", "production_item", "status", "company"]:
		if filters.get(field):
			query_filters[field] = ("in", filters.get(field))

	query_filters["planned_start_date"] = (">=", filters.get("from_date"))
	query_filters["planned_end_date"] = ("<=", filters.get("to_date"))

	data = frappe.get_all(
		"Work Order", fields=fields, filters=query_filters, order_by="planned_start_date asc"
	)

	res = []
	items=[]
	ans= {}
	for i in items:
		ans[i]={"production_item":i,"qty":0,"produced_qty":0,"lead_time":0}
	for d in data:
		items.append(d.production_item)
		start_date = d.actual_start_date or d.planned_start_date
		d.age = 0

		if d.status != "Completed":
			d.age = date_diff(today(), start_date)

		if filters.get("age") <= d.age:
			res.append(d)
	items=list(set(items))
	total_produced_qty=0
	max_name=""
	max_value=-1
	min_name=""
	min_value=99999999999
	for i in items:
		ans[i] = {"production_item":i,"qty":0,"produced_qty":0,"lead_time":0}
	total_today=0
	now=frappe.utils.get_datetime()
	for d in data:
		start_date = d.actual_end_date or d.planned_end_date
		diff=date_diff(start_date,now)
		if diff==0:
			total_today+=d.produced_qty
		row=ans[d.production_item]
		row["qty"]=row["qty"]+d.qty
		row["produced_qty"]=row["produced_qty"]+d.produced_qty
		total_produced_qty+=d.produced_qty
		row["lead_time"]=row["lead_time"]+d.lead_time
		ans[d.production_item]=row
	ans2=[]
	labels=[]
	values=[]
	values2=[]
	for r in items:
		ans2.append(ans[r])
		qty=ans[r]["produced_qty"]
		values2.append(ans[r]["qty"])
		if qty > max_value:
			max_value=qty
			max_name=r
		if qty < min_value:
			min_value=qty
			min_name=r
		values.append(qty)
	total_qty=sum(values2)
	if max_value==-1:
		max_value=0
	chart = {'data':{'labels':items,'datasets':[{'name':'Produced Qty','values':values}] },"type":"bar","colors":["#03befc"]}
	return {"total_qty":total_qty,"res":ans2,"total_today":total_today,"total_items":len(items),"total_produced_qty":total_produced_qty,"chart":chart,"max_produced_qty":max_value,"max_name":max_name}


def get_chart_data(data, filters):
	if filters.get("charts_based_on") == "Status":
		return get_chart_based_on_status(data)
	elif filters.get("charts_based_on") == "Age":
		return get_chart_based_on_age(data)
	else:
		return get_chart_based_on_qty(data, filters)


def get_chart_based_on_status(data):
	labels = frappe.get_meta("Work Order").get_options("status").split("\n")
	if "" in labels:
		labels.remove("")

	status_wise_data = defaultdict(int)

	for d in data:
		status_wise_data[d.status] += 1

	values = [status_wise_data[label] for label in labels]

	chart = {
		"data": {"labels": labels, "datasets": [{"name": "Qty Wise Chart", "values": values}]},
		"type": "donut",
		"height": 300,
	}

	return chart


def get_chart_based_on_age(data):
	labels = ["0-30 Days", "30-60 Days", "60-90 Days", "90 Above"]

	age_wise_data = {"0-30 Days": 0, "30-60 Days": 0, "60-90 Days": 0, "90 Above": 0}

	for d in data:
		if d.age > 0 and d.age <= 30:
			age_wise_data["0-30 Days"] += 1
		elif d.age > 30 and d.age <= 60:
			age_wise_data["30-60 Days"] += 1
		elif d.age > 60 and d.age <= 90:
			age_wise_data["60-90 Days"] += 1
		else:
			age_wise_data["90 Above"] += 1

	values = [
		age_wise_data["0-30 Days"],
		age_wise_data["30-60 Days"],
		age_wise_data["60-90 Days"],
		age_wise_data["90 Above"],
	]

	chart = {
		"data": {"labels": labels, "datasets": [{"name": "Qty Wise Chart", "values": values}]},
		"type": "donut",
		"height": 300,
	}

	return chart


def get_chart_based_on_qty(data, filters):
	labels, periodic_data = prepare_chart_data(data, filters)

	pending, completed = [], []
	datasets = []

	for d in labels:
		pending.append(periodic_data.get("Pending").get(d))
		completed.append(periodic_data.get("Completed").get(d))

	datasets.append({"name": "Pending", "values": pending})
	datasets.append({"name": "Completed", "values": completed})

	chart = {
		"data": {"labels": labels, "datasets": datasets},
		"type": "bar",
		"barOptions": {"stacked": 1},
	}

	return chart


def prepare_chart_data(data, filters):
	labels = []

	periodic_data = {"Pending": {}, "Completed": {}}

	filters.range = "Monthly"

	ranges = get_period_date_ranges(filters)
	for from_date, end_date in ranges:
		period = get_period(end_date, filters)
		if period not in labels:
			labels.append(period)

		if period not in periodic_data["Pending"]:
			periodic_data["Pending"][period] = 0

		if period not in periodic_data["Completed"]:
			periodic_data["Completed"][period] = 0

		for d in data:
			if getdate(d.planned_start_date) >= from_date and getdate(d.planned_start_date) <= end_date:
				periodic_data["Pending"][period] += flt(d.qty) - flt(d.produced_qty)
				periodic_data["Completed"][period] += flt(d.produced_qty)

	return labels, periodic_data


def get_columns(filters):
	columns=[]

	columns.extend(
		[
			{
				"label": _("Production Item"),
				"fieldname": "production_item",
				"fieldtype": "Link",
				"options": "Item",
				"width": 150,
			},
			{"label": _("Produce Qty"), "fieldname": "qty", "fieldtype": "Float", "width": 150},
			{"label": _("Produced Qty"), "fieldname": "produced_qty", "fieldtype": "Float", "width": 150}
		]
	)

	if not filters.get("status"):
		columns.append({"label": _("Status"),"fieldname":"status","width":110})

	if False and filters.get("status") != "Not Started":
		columns.extend(
			[
				{
					"label": _("Actual Start Date"),
					"fieldname": "actual_start_date",
					"fieldtype": "Date",
					"width": 100,
				},
				{
					"label": _("Actual End Date"),
					"fieldname": "actual_end_date",
					"fieldtype": "Date",
					"width": 100,
				},
				{"label": _("Age"), "fieldname": "age", "fieldtype": "Float", "width": 110},
			]
		)

	if filters.get("status") == "Completed":
		columns.extend(
			[
				{
					"label": _("Lead Time (in mins)"),
					"fieldname": "lead_time",
					"fieldtype": "Float",
					"width": 180,
				},
			]
		)

	return columns
