frappe.listview_settings['Store Item'] = {
	  add_fields: [ 'status'],

	 get_indicator(doc) {
		if(doc.status=="publish"){ return [__("Publish"), "green", "status,=,publish"];}
		else if(doc.status=="private"){ return [__("Private"), "gray", "status,=,private"];}
		else if(doc.status=="draft"){ return [__("Draft"), "red", "status,=,draft"];}
		else { return [__("Pending"), "orange", "status,=,pending"];}
	}

}
