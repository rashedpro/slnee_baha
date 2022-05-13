# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import print_function, unicode_literals

import frappe

no_cache = 1


def get_context(context):
	if frappe.flags.in_migrate:
		return
	context.http_status_code = 500
	try:
		context["button_color"]=frappe.get_doc("Website Settings").button_color
	except:
		context["button_color"]="#2595ec"
	if not context["button_color"]:
		context["button_color"]="#2595ec"

	print(frappe.get_traceback())
	return {"error": frappe.get_traceback().replace("<", "&lt;").replace(">", "&gt;")}
