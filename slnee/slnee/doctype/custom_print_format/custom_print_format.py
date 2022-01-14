# Copyright (c) 2021, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CustomPrintFormat(Document):
	def validate(self):
		self.jinja_check()
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
					html=html[:pos+l+4]+" {% if not ("+i.display_depends_on+") %}hide1 {% endif %}"+html[pos+l+4:]
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
				html=html[:pos+11]+" {% if not ("+self.display_qr+") %}hide1 {% endif %}"+html[pos+11:]
			doc.html=html
			doc.css=css
			doc.disabled=self.is_disabled
			doc.save()

	
	pass



	def jinja_check(self):
		from jinja2 import Template
		if (self.display_qr!= None and self.display_qr != ""):
			text=self.display_qr
			try :
				tm= Template("{{ "+text+" }}" )
				msg = (tm.render())
			except Exception as err :
				if "'doc' is undefined" in str(err):
					p = text.find("doc.")+4
					field=""
					for i in range(p,len(text)+1):
						if i == len(text) or (not text[i].isalnum()  and text[i] != "_") :
							field=text[p:i]
							break
					meta = frappe.get_meta(self.doc_type)
					if not meta.has_field(field):
						frappe.msgprint("Invalid 'depends_on' expression in QR Code",raise_exception=False)
						frappe.msgprint(("Doctype {0} has no attribute {1}").format(self.doc_type,field),raise_exception = True )
				else:
					frappe.msgprint("Invalid 'depends_on' expression in QR Code",raise_exception=False)
					frappe.msgprint(("{0}").format(err),raise_exception = True )


		for i in self.header_elements+self.body_elements+self.footer_elements:
			if (i.display_depends_on != None and i.display_depends_on !=""):
				text = i.display_depends_on
				try :
					tm= Template("{{ "+i.display_depends_on+" }}" )
					msg = (tm.render())
				except Exception as err :
					if "'doc' is undefined" in str(err):
						p = text.find("doc.")+4
						field=""
						if p==len(text):
							field=text[p-1]
						else:
							for j in range(p,len(text)+1):
								if j == len(text) or (not text[j].isalnum() and text[j] != "_" ) :
									field=text[p:j]
									break
						meta = frappe.get_meta(self.doc_type)
						if not meta.has_field(field):
							frappe.msgprint(("Invalid 'depends_on' expression in {0}, row {1}").format(i.parentfield,i.idx),raise_exception=False)
							frappe.msgprint(("Doctype {0} has no attribute {1}").format(self.doc_type,field),raise_exception = True )

					else:
						frappe.msgprint(("Invalid 'depends_on' expression in {0}, row {1}").format(i.parentfield,i.idx),raise_exception=False)
						frappe.msgprint(("{0}").format(err),raise_exception = True )

