// Copyright (c) 2022, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Server', {
	refresh: function(frm) {

	frappe.call({
                method:"activity_today",
                doc:frm.doc,
                callback(r){
			console.log(r.message);
			console.log("baha");
		}})


	frappe.call({
                method:"heat_map",
                doc:frm.doc,
                callback(r){
	if (r.message) {
	const startDate = new Date();
	startDate.setFullYear(2021,3,11);

	const endDate = new Date();

	let data = {
    dataPoints: r.message,
   // start: startDate, // a JS date object
   // end: endDate
}

	let chart = new frappe.Chart("#heatmap", {
    type: 'heatmap',
    data: data})

}
}})

	},

	open: function(frm) {  

	if (frm.doc.docstatus == 1 ) {
		window.open(frm.doc.url);
}
}




});
