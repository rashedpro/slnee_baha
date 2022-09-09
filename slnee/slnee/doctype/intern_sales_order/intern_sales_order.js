// Copyright (c) 2022, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Intern Sales Order', {
	 refresh: function(frm) {
		if (frm.doc.name.includes("new")){frm.set_value("status","Draft");refresh_field("status") };

		if (frm.doc.docstatus==1 && (frm.doc.status=="Open" || frm.doc.status=="Partially Manufactured")){
			frm.add_custom_button(__('Work Order'), () => make_work_order(frm), __('Create'));
	 }},
	required_by :function(frm) {
		for (var i =0;i<frm.doc.items.length;i++){
			frm.doc.items[i].schedule_date=frm.doc.required_by;
		}
		refresh_field("items");

	}
});




frappe.ui.form.on('Intern Sales Order ITem', {
	item_code(frm,cdt,cdn){
		var row=locals[cdt][cdn];
		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype : "Item",
				name : row.item_code,
			},
			callback(r){
				if (r.message) {
					var i = r.message;
					row.description=i.description;
					row.uom=i.stock_uom;
					row.stock_uom=i.stock_uom;
					row.item_name=i.item_name;
					row.qty=1;
					row.conversion_factor=1;
					if (frm.doc.required_by){row.schedule_date=frm.doc.required_by};
					refresh_field("items");
				}
			}
		})
	}
});





function make_work_order(frm){
	console.log("work_order");
	var me = this;
		frm.call({
			doc: frm.doc,
			method: 'get_work_order_items',
			callback: function(r) {
				if(!r.message) {
					frappe.msgprint({
						title: __('Work Order not created'),
						message: __('No Items with Bill of Materials to Manufacture'),
						indicator: 'orange'
					});
					return;
				}
				else if(!r.message) {
					frappe.msgprint({
						title: __('Work Order not created'),
						message: __('Work Order already created for all items with BOM'),
						indicator: 'orange'
					});
					return;
				} else {
					const fields = [{
						label: 'Items',
						fieldtype: 'Table',
						fieldname: 'items',
						description: __('Select BOM and Qty for Production'),
						fields: [{
							fieldtype: 'Read Only',
							fieldname: 'item_code',
							label: __('Item Code'),
							in_list_view: 1
						}, {
							fieldtype: 'Link',
							fieldname: 'bom',
							options: 'BOM',
							reqd: 1,
							label: __('Select BOM'),
							in_list_view: 1,
							get_query: function (doc) {
								return { filters: { item: doc.item_code } };
							}
						}, {
							fieldtype: 'Float',
							fieldname: 'pending_qty',
							reqd: 1,
							label: __('Qty'),
							in_list_view: 1
						}, {
							fieldtype: 'Data',
							fieldname: 'sales_order_item',
							reqd: 1,
							label: __('Sales Order Item'),
							hidden: 1
						}],
						data: r.message,
						get_data: () => {
							return r.message
						}
					}]
					var d = new frappe.ui.Dialog({
						title: __('Select Items to Manufacture'),
						fields: fields,
						primary_action: function() {
							var data = {items: d.fields_dict.items.grid.get_selected_children()};
							frm.call({
								method: 'make_work_orders',
								args: {
									items: data,
									company: frm.doc.company,
									sales_order: frm.doc.name,
									project: ''
								},
								freeze: true,
								callback: function(r) {
									if(r.message) {
										frappe.msgprint({
											message: __('Work Orders Created: {0}', [r.message.map(function(d) {
													return repl('<a href="/app/work-order/%(name)s">%(name)s</a>', {name:d})
												}).join(', ')]),
											indicator: 'green'
										})
									}
									d.hide();
								}
							});
						},
						primary_action_label: __('Create')
					});
					d.show();
				}
			}
		});
	}


