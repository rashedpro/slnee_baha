# Copyright (c) 2021, Weslati Baha Eddine and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class Font(Document):
	def validate(self):
		if self.type =="Google Fonts" :
			self.css=self.googlelinks
		if self.type=="Otf file":
			if self.is_url==1:
				self.css="""
<style>
@font-face {
font-family:"""+ self.name+""";
src:url('"""+self.file_link+"""');
}
</style>
"""
			else:
				self.css="""
<style>
@font-face {
font-family:"""+ self.name+""";
src:url('"""+self.file+"""');
}
</style>
"""


	pass
