// Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */


console.log("baha");
const style = document.createElement('style');
style.textContent = " .summary-item {min-width:150px !important; } "
document.head.appendChild(style);


frappe.query_reports["Employee Summary"] = {
	"filters": [
		{
			fieldname:'company',
			label: __('Company'),
			fieldtype: 'Link',
			options: 'Company',
			default: frappe.defaults.get_user_default('Company')
		},
		 {
                        fieldname:'employee',
                        label: __('Employee'),
                        fieldtype: 'Link',
                        options: 'Employee'
                },
		{
			fieldname:'designation',
			label: __('Designation'),
			fieldtype: 'Link',
			options: 'Designation',
		},
		{
                        fieldname:'nationality',
                        label: __('Nationality'),
                        fieldtype: 'Link',
                        options: 'Country',
                },
		{
			fieldname:'on_leave',
			label: __('On leave'),
			fieldtype: 'Select',
			options: ["","Yes","No"]
		},
		{
                        fieldname:'greater_than',
                        label: __('Salary Greater Than'),
                        fieldtype: 'Data'
                },
		{
                        fieldname:'status',
                        label: __('Status'),
                        fieldtype: 'MultiSelectList',
                        options: ["Active","Inactive","Suspended","Left"]
                },
	]
};
