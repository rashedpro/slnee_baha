// Copyright (c) 2022, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Deduction', {
	// refresh: function(frm) {

	// }

	setup: function(frm) {
		frm.set_query("component", function() {
			return {
				filters: [
					["Salary Component","type", "in", ["Deduction"]]
				]
			}
		});
	}

});
