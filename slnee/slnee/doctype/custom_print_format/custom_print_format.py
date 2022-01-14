# Copyright (c) 2021, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CustomPrintFormat(Document):
	def validate(self):
		if frappe.db.exists("Print Format",self.name) ==None:
			html=""
			css= self.css if self.css else ""
			css+="""
	thead {display: table-header-group; }
tfoot {display: none; }
@media print {
.print-format {
margin-left: 0mm;
margin-right: 0mm;
}
#footer-html{
display:block;
}
.page-footer{
position:fixed;
bottom:0mm;
}
html,body{
padding-bottom:0mm;
}
}
.print-format {
padding: 0in;
}

@media screen{
.page-footer{display:none;}
}
@page  
{size: auto; 
 margin: 0mm 0mm 0mm 0mm;  
} 
.hide1{display:none;}
"""
			if self.links:
				html+=self.links
			if self.html:
				html+=self.html
			for i in self.header_elements +self.body_elements+self.footer_elements:
				if (i.display_depends_on != None and i.display_depends_on !=""):
					pos=html.find("code"+i.name)
					l=len(str(i.name))
					html=html[:pos+l+4]+" {% if not "+i.display_depends_on+" %}hide1 {% endif %}"+html[pos+l+4:]
			if (self.display_qr!= None and self.display_qr != ""):
				pos=html.find("codeqr_code")
				html=html[:pos+11]+" {% if not ("+self.display_qr+") %}hide1 {% endif %}"+html[pos+11:]
			doc = frappe.get_doc({
				'doctype':'Print Format',
				"name":self.name,
				'doc_type':self.doc_type,
				"disabled":self.is_disabled,
				"html":html,
				"css":css,
				"Standard": "No",
				"custom_format":1,
				"print_format_type":"Jinja"}).insert(ignore_if_duplicate=True)
		else:
			doc=frappe.get_doc("Print Format",self.name)
			html=""
			css= self.css if self.css else ""
			css+="""
thead {display: table-header-group; }
tfoot {display: none; }
@media print {
.print-format {
margin-left: 0mm;
margin-right: 0mm;
}
#footer-html{
display:block;
}
.page-footer{
position:fixed;
bottom:0mm;
}
html,body{
padding-bottom:0mm;
}
}
.print-format {
padding: 0in;
}

@media screen{
.page-footer{display:none;}
}
@page  
{size: auto; 
 margin: 0mm 0mm 0mm 0mm;  
} 
.hide1{display:none;}
"""
			if self.links:
				html+=self.links
			if self.html:
				html+=self.html
			for i in self.header_elements+self.body_elements+self.footer_elements:
				if (i.display_depends_on != None and i.display_depends_on !=""):
					pos=html.find("code"+i.name)
					l=len(str(i.name))
					html=html[:pos+l+4]+" {% if not ("+i.display_depends_on+") %}hide1 {% endif %}"+html[pos+l+4:]


			if (self.display_qr!= None and self.display_qr != ""):
				pos=html.find("codeqr_code")
				html=html[:pos+11]+" {% if not "+self.display_qr+" %}hide1 {% endif %}"+html[pos+11:]
			doc.html=html
			doc.css=css
			doc.disabled=self.is_disabled
			doc.save()

	
	pass
