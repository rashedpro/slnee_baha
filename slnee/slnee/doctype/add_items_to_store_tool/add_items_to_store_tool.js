// Copyright (c) 2022, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Add Items to Store Tool', {
	refresh: function(frm) {
		frm.call({
			doc:frm.doc,
			method: 'set_defaults'})
	//$(".btn-primary").hide();
	//$(".indicator-pill").hide();
	},
	item_group: function(frm){refresh_items(frm)},
	have_price_list: function(frm){refresh_items(frm)},
	in_stock: function(frm){refresh_items(frm)},
	insert:function(frm){insert_items(frm)},
});

frappe.ui.form.on("Store Item List",{

	item(frm,cdt,cdn){
		let row = frappe.get_doc(cdt, cdn);
		console.log("item added");
		}


})



function insert_items(frm){
	frm.call({
		doc:frm.doc,
		method: 'insert_items',
		freeze:true,
		freeze_message: __("Inserting Items"),
	})
};
function refresh_items(frm){
	frm.call({
		doc:frm.doc,
		args:{"item_group":frm.doc.item_group},
		freeze: true,
		freeze_message: __("Fetching Items"),
		method: 'get_items',
		})
}
