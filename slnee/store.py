import frappe
from slnee.slnee.doctype.wordpress_store.wordpress_store import get_api


def update_stock():
	update=[]
	l=frappe.db.get_list("Store Item",filters={"type":simple},fields=["id"])
