// Copyright (c) 2022, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Store Item', {
	 refresh: function(frm) {
		frm.add_custom_button(__("Open Link"), function() {
			if (frm.doc.permalink != "" ){
			window.open(frm.doc.permalink,'_blank');}

		})
	 }
});
