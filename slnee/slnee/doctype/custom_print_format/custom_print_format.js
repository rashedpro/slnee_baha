// Copyright (c) 2021, Weslati Baha Eddine and contributors
// For license information, please see license.txt


frappe.ui.form.on('Custom Print Format', {
	 refresh: function(frm) {
		first_creation(frm);
var slider = document.getElementById("input-range");
slider.value=frm.doc.height;
slider.oninput = function() {
frm.set_value("height",this.value);
refresh_field("height");
//output.innerHTML = this.value;
}

	 }
});


frappe.ui.form.on('Custom Print Format', {
	height: function(frm){
		if (frm.doc.height<=0){
			frm.set_value("show","No");
			refresh_field('show');
			frm.set_value("height",10);
			refresh_field("height");}
		else if (frm.doc.height>200){
			frm.set_value("height",200);
			document.getElementById("input-range").value=200;
			refresh_field("height");}
		else {
			document.getElementById("header").height=frm.doc.height;}

	}
});

frappe.ui.form.on('header_elements','Width',function(frm,cdt,cdn) {

console.log(cdt);
});

function head_elements(frm){
frm.doc.elements.forEach(function(element){
console.log("1");

});

}

function place(element,parent_id){
	if (element.disabled == 0) {
		var parent = document.getElementById(parent_id);
		if (element.is_image == 0){
			var element_ = document.createElement("div");
			$('head').append("<style>.text_element{touch-action:none;border: dashed 1px #CCC;}</style>")
			element_.classList.add("text_element");
			element_.classList.add('resize-drag');
			element_.style.position="absolute";
			element_.style.color=element.color;
			if (element.font){
				frappe.call({
					method : "frappe.client.get",
					args:{
						"doctype":"Font",
						"name":element.font},
					callback(r) {
						if(r.message){
							var css = r.message.css;console.log(css);$('head').append(css);}
						}
					});
				
				element_.style.fontFamily = "'"+element.font+"',sans-serif";}
			element_.innerHTML=element.label;
			element_.style.top=element.y.toString()+"px";
			if (element.center ==0){
				element_.style.left=element.x.toString() + "px";}
			else{
                                element_.style.left="50%";
				element_.style.transform= "translate(-50%,0)";
			}
			var size=element.width;
			if ( element.height < element.width) {size=element.height;}
			element_.style.fontSize=size.toString()+"px";
			parent.appendChild(element_);}

		else{	//image 
			var element_ = document.createElement("img");
			$('head').append("<style>.image_element{touch-action:none;border: dashed 1px #CCC;}</style>")
                        element_.classList.add("image_element");
                        element_.classList.add('resize-drag');
			element_.style.position="absolute";
			element_.src = element.image;
                        element_.style.top=element.y.toString()+"px";
                        if (element.center ==0){
                                element_.style.left=element.x.toString() + "px";}
                        else{
                                element_.style.left="50%";
                                element_.style.transform= "translate(-50%,0)";
                        }
		}
			element_.style.width=element.width.toString()+"px";
			element_.style.height=element.height.toString()+"px";
                        parent.appendChild(element_);
			
				}
}


function first_creation(frm){
	fix_header(frm)
	frm.doc.header_elements.forEach(function(element){
		place(element,"headspace")
		});
}


function fix_header(frm){

				frappe.call({
                                        method : "frappe.client.get",
                                        args:{
                                                "doctype":"test1",
                                                "name":"89dafd0b98"},
                                        callback(r) {
                                                if(r.message){
                                                        var css = r.message.name1;console.log(css);$('head').append(css);}
                                                }
                                        });


	if (frm.doc.show != "No"){
		var header =  document.getElementById("headspace");
		header.style.display="block";
		header.style.borderColor=frm.doc.border_color;
		header.style.borderStyle=frm.doc.border;
		//header.style.borderWidth:frm.doc.
		header.style.height=frm.doc.height.toString()+"px";
				}
	else{var header =  document.getElementById("header");
                header.style.display="none";}
}


