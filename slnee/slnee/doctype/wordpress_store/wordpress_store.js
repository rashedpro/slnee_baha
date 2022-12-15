// Copyright (c) 2022, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Wordpress Store', {
	 refresh: function(frm) {
		 frm.add_custom_button(__("Fetch Orders"), function() {
			frm.call({
			doc:frm.doc,
			freeze: true,
			freeze_message: __("Fetching Orders, please wait."),
			method: "get_orders",
			})
		})
	 },
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
	get_attributes : function(frm){
		frm.call({
			doc:frm.doc,
			freeze:true,
			freeze_message: __("Fetching Attributes, please wait."),
			method: "get_attributes",
			})},
	get_categories : function(frm){
		frm.call({
			doc:frm.doc,
			freeze:true,
			freeze_message: __("Fetching Categories, please wait."),
			method: "get_categories",
			})},
	get_products : function(frm){
		frm.call({
			doc:frm.doc,
			freeze:true,
			freeze_message: __("Fetching Products, please wait."),
			method: "get_products",
			})},
	get_customers :  function(frm){
		frm.call({
			doc:frm.doc,
			freeze: true,
			freeze_message: __("Fetching Customers, please wait."),
			method: "get_customers",
			})},
	get_orders : function(frm){
		frm.call({
			doc:frm.doc,
			freeze: true,
			freeze_message: __("Fetching Orders, please wait."),
			method: "get_orders",
			})},
	sales_taxes_and_charges_template : function(frm){
		console.log("taxes");
		frm.call({
			doc:frm.doc,
			method: "get_taxes",
			})
		frm.refresh_field("taxes");
	}
});
