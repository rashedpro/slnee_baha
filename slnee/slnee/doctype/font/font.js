// Copyright (c) 2021, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Font', {
	 refresh: function(frm) {
		//set slider font-size
                var slider = document.getElementById("input-range");
		slider.value=40;
		document.getElementById("prv").style.fontSize="40px";
                slider.oninput = function() {
                        var element = document.getElementById("prv");
                        element.style.fontSize=this.value.toString()+"px";
			document.getElementById("size").innerHTML=this.value.toString()+"px";
                }


		//fix preview text
		console.log(frm.doc.preview_text);
		if (frm.doc.preview_text=="" || frm.doc.preview_text==undefined){
			if(frm.doc.language=="English"){
				frm.set_value("preview_text","A journey of a thousand miles begins with a single step.")
			}

		}
		set_preview(frm);
	 }
});



function set_preview(frm){
	$('head').append(frm.doc.css);
 	var element = document.createElement("div");
        element.innerHTML=frm.doc.preview_text;
        element.style.fontFamily = frm.doc.name;
        var parent = document.getElementById("prv");
        parent.innerHTML="";
        parent.appendChild(element);

}


frappe.ui.form.on('Font', {
	preview_text: function(frm){set_preview(frm);}
});
frappe.ui.form.on('Font', {
        googlelinks: function(frm){set_preview(frm);}
});
frappe.ui.form.on('Font', {
        name1: function(frm){set_preview(frm);}
});


frappe.ui.form.on('Font', {
	language: function(frm){
		if (frm.doc.language=="العربية"){
			frm.set_value("preview_text","بسم الله الرحمن الرحيم ")
			refresh_field("preview_text");
		}
		else if (frm.doc.language=="English"){
                        frm.set_value("preview_text","A journey of a thousand miles begins with a single step.")
                        refresh_field("preview_text");
                }

	}
});
