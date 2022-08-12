// Copyright (c) 2022, Weslati Baha Eddine and contributors
// For license information, please see license.txt
/* eslint-disable */
const style = document.createElement('style');

style.textContent = " .summary-value{line-height:22px !important; } "

document.head.appendChild(style);

frappe.query_reports["tax declaration"] = {
        "filters": [
                {
                        fieldname: "type",
                        label: __("Type"),
                        fieldtype: "Select",
                        options : [__("Sales"),__("Purchases")],
                        default: __("Sales"),
                        reqd: 1
                },

                {
                        fieldname: "company",
                        label: __("Company"),
                        fieldtype: "Link",
                        options: "Company",
                        default: frappe.defaults.get_user_default("Company"),
                        reqd: 1
                },

                {
                        fieldname: "from_date",
                        label: __("From Date"),
                        fieldtype: "Date",
                        default: frappe.defaults.get_user_default("year_start_date"),
                        reqd: 1
                },
                {
                        fieldname:"to_date",
                        label: __("To Date"),
                        fieldtype: "Date",
                        default: frappe.defaults.get_user_default("year_end_date"),
                        reqd: 1
                }



        ]
};
