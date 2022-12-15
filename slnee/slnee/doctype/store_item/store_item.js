// Copyright (c) 2022, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Store Item', {
	 refresh: function(frm) {
		frm.add_custom_button(__("Open Link"), function() {
			if (frm.doc.permalink && frm.doc.permalink != "" ){
			window.open(frm.doc.permalink,'_blank');}
			else{
				frappe.msgprint(__('Item not synchronized to store'));
			}

		}),
		frm.add_custom_button(__("Reload from Store"), function() {
		

		}),
		frm.add_custom_button(__("Sync to Store"), function() {
			frappe.msgprint({
				title: __('Sync'),
				message: __('Are you sure you want to Sync data with the store?'),
				primary_action:{
					 action(values) {
						cur_dialog.hide();
						frappe.call({
							async:false,
							doc:frm.doc,
							args:{"show_alert":true},
							method:"sync_to_store",
							//freeze: true,
							//freeze_message: __("synchronizing"),
							callback(r) {if(r.message){ frm.reload_doc();refresh_field("last_sync") }}
						})
					}
				}
			});
		});
	 },
	has_variants: function(frm){
		if(frm.doc.has_variants){frm.set_value("type","variable")}
		else{frm.set_value("type","simple")}
		refresh_field("type")


	},
	warehouse: function(frm){
		var warehouses=[];
		if (frm.doc.warehouse){
			for (var i=0;i<frm.doc.warehouse.length;i++){
				warehouses.push(frm.doc.warehouse[i].warehouse)
		}}
		console.log("warehouse chanegd")
		for (var i=0;i<frm.doc.items.length;i++){
			var item=frm.doc.items[i];
			frappe.call({
				async:false,
				args:{"item":item.item,"warehouse":warehouses},
				method:"slnee.slnee.doctype.store_item.store_item.get_item_info",
				callback(r) {
					if(r.message){
						var ans=r.message.split("#");
						item.price=parseFloat(ans[0]);
						item.tax=parseFloat(ans[2])
						item.stock=parseFloat(ans[1]);
						//item.warehouse=frm.doc.warehouse;
					}
				}
			})
		}
			frm.refresh_field("items");
			set_total_price(frm);
	}
});
	frappe.ui.form.on('Store Item List','item' ,function(frm,cdt,cdn){
		var item = locals[cdt][cdn];
		var warehouses=[];
		if (frm.doc.warehouse){
		for (var i=0;i<frm.doc.warehouse.length;i++){
			warehouses.push(frm.doc.warehouse[i].warehouse)
		}}
		console.log(warehouses);
		frappe.call({
			args:{"item":item.item,"warehouse":warehouses},
			method:"slnee.slnee.doctype.store_item.store_item.get_item_info",
			callback(r) {
				if(r.message){
					var ans=r.message.split("#");
					item.price=parseFloat(ans[0]);
					item.stock=parseFloat(ans[1]);
					item.tax=parseFloat(ans[2])
					//item.warehouse=frm.doc.warehouse;
					frm.refresh_field("items");
					set_total_price(frm);
				}
			}
		})


});
frappe.ui.form.on('Store Item List','price' ,function(frm,cdt,cdn){
	set_total_price(frm);
});
frappe.ui.form.on('Store Item List','stock' ,function(frm,cdt,cdn){
	set_total_price(frm);
});
frappe.ui.form.on('Store Item List','sale_price' ,function(frm,cdt,cdn){
	set_total_price(frm);
});
frappe.ui.form.on('Store Item List', {
	items_remove(frm,cdt,cdn){
		set_total_price(frm);
	}
});
function set_total_price(frm){
	frappe.call({
		method:"slnee.slnee.doctype.store_item.store_item.get_tax_per",
		callback(r) {if(r.message){ frm.set_value("tax_per",parseFloat(r.message));refresh_field("tax_per");}
		}
	})
	var price=0;
	var sale=0;
	var total_tax=0;
	var stock=9999999999999;
		for (var i =0;i<frm.doc.items.length;i++){
			price=price+frm.doc.items[i].price;
			sale=sale+frm.doc.items[i].sale_price;
			stock=Math.min(stock,frm.doc.items[i].stock)
		}
		total_tax=(price*frm.doc.tax_per);
		var sale_tax=sale*frm.doc.tax_per;
		if (stock==9999999999999){stock=0;}
		frm.set_value("tax",total_tax);refresh_field("total_tax");
		frm.set_value("sale_price",sale+sale_tax);refresh_field("sale_price");
		frm.set_value("stock_quantity",stock);refresh_field("stock_quantity");
		frm.set_value("regular_price",price+total_tax);refresh_field("regular_price");
		console.log(sale);
		if (sale >0){frm.set_value("on_sale",1)}else{frm.set_value("on_sale",0)};refresh_field("on_sale");
		//if (stock >0){frm.set_value("manage_stock",1)}else{frm.set_value("manage_stock",0)}
		//refresh_field("manage_stock");
}
