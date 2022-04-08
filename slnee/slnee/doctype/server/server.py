# Copyright (c) 2022, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
class Server(Document):



	def on_submit(self):
		url=self.url
		url+="/api/method/frappe.auth.get_logged_user"
		headers=self.headers()
		print(100*"5")
		print(url)
		print(headers)
		response = requests.request("GET", url, headers=headers)
		print(response)
		if int(response.status_code) !=200 :
			frappe.msgprint("Connection failed !",raise_exception = True)
		frappe.msgprint("Connected.",raise_exception = False)


	def headers(self):
		return {"Authorization":"token "+str(self.api_key)+":"+str(self.api_secret)}
	@frappe.whitelist()
	def heat_map(self):
		url=self.url
		url+="/api/method/frappe.desk.page.activity.activity.get_heatmap_data"
		response = requests.request("GET", url, headers=self.headers())
		d={}
		from datetime import datetime
		print(response.text)
		try:
			return(response.json()["message"])
			for i in response.json()["message"]:
				ts=response.json()["message"][i]
				t = datetime.utcfromtimestamp(int(i))
				d[t]=ts
			return(d)
		except:
			return()
	@frappe.whitelist()
	def heat_count(self,):
		d=self.heat_map()
		c=0
		for i in d:
			c+=d[i]
		return(c)
	@frappe.whitelist()
	def refresh(self):
		print(self.name)

		return(55)
	@frappe.whitelist()
	def activity_today(self):
		return("baha")


	pass

