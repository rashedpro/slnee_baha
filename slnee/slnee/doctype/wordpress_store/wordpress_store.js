// Copyright (c) 2022, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Wordpress Store', {
	// refresh: function(frm) {

	// }
	test : function(frm){
		frm.call({
			doc:frm.doc,
			method: 'test',
			callback: function(r){
				if (r.message=="Connected to server."){
					frappe.msgprint({title: __('Status'), indicator: 'green',message : __(r.message)});
				}else{
					 frappe.msgprint({title: __('Status'),indicator:'red',message : __(r.message)});
				}
}
		})
	},
	get_categories : function(frm){
		frm.call({
			doc:frm.doc,
			method: "get_categories",
			})



	}
});
