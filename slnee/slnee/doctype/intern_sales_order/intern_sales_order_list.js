frappe.listview_settings['Intern Sales Order'] = {
	 add_fields: ['status'],
	 hide_name_column: true,
	 get_indicator(doc) {
		//return [__("Test"), "completed", "status,=,Completed"];
		  if (doc.status=="Draft") {  return [__("Draft"), "red", "status,=,Drat"];}
		else if (doc.status=="Manufactured") {  return [__("Manufactured"),"green", "status,=,Manufactured"];}
		else if (doc.status=="Open") {  return [__("Open"), "orange", "status,=,Open"];}
		else if (doc.status=="Partially Manufactured") {  return [__("Partially Manufactuerd"), "pink", "status,=,Partially Manufactured"];}
		else{  return [__("Cancelled"), "red", "status,=,Cancelled"];}
	}








}
