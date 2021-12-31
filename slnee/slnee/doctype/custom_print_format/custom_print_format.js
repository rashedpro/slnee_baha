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
        before_save: function(frm){
	var cont =document.getElementById("my_container");
	frm.set_value("html",cont.innerHTML);
	refresh_field("html");
	save_header_elements(frm);
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
			document.getElementById("header").style.height=frm.doc.height.toString()+"px";}

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

function place(element,parent_id,frm){
	if (element.disabled == 0) {
		var parent = document.getElementById(parent_id);
		if (element.is_image == 0){ //label
			var element_ = document.createElement("div");
			add_css(frm,".text_element{touch-action:none;border: dashed 1px #CCC;}");
			element_.classList.add("text_element");
			element_.style.color=element.color;
			if (element.font){
				frappe.call({
					method : "frappe.client.get",
					args:{
						"doctype":"Font",
						"name":element.font},
					callback(r) {
						if(r.message){add_links(frm,r.message.css);}
						}
					});
			element_.style.fontFamily = "'"+element.font+"',sans-serif";}
			element_.innerHTML=element.label;}

		else{	//image
			var element_ = document.createElement("img");
			add_css(frm,".image_element{touch-action:none;border: dashed 1px #CCC;}");
                        element_.classList.add("image_element");
			element_.src = element.image;
		}
			element_.style.top=element.y.toString()+"px";
                        element_.style.left=element.x.toString()+"px";
                        element_.setAttribute("data-x",element.x);
                        element_.setAttribute("data-y",element.y);
			element_.classList.add('resize-drag');
                        element_.style.position="absolute";
			element_.style.width=element.width.toString()+"px";
			element_.style.height=element.height.toString()+"px";
			element_.setAttribute("id",element.name);
                        parent.appendChild(element_);
	}
}


function first_creation(frm){
	fix_header(frm)
	frm.doc.header_elements.forEach(function(element){
		place(element,"headspace",frm)
		});
}


function fix_header(frm){
	if (frm.doc.show != "No"){
		var header =  document.getElementById("header");
		header.style.display="block";
		header.style.borderColor=frm.doc.border_color;
		header.style.borderStyle=frm.doc.border;
		//header.style.borderWidth:frm.doc.
		header.style.height=frm.doc.height.toString()+"px";
				}
	else{var header =  document.getElementById("header");
                header.style.display="none";}
}


function add_css(frm,css){
	$('head').append("<style>"+css+"</style>")
	var old_css=frm.doc.css;
	if (!old_css.includes(css)){
	frm.set_value("css",old_css+css);
        refresh_field("css");
	}

}

function add_links(frm,links){
	$('head').append(links)
        var old_links=frm.doc.links;
	if (old_links==undefined){var old_links="";}
        if (!old_links.includes(links)){
        frm.set_value("links",old_links+links);
        refresh_field("links");
        }

}

function save_element(frm,element_id){
	var element =  document.getElementById(element_id);
	frappe.model.set_value("div",element_id,"height",element.offsetHeight);
	frappe.model.set_value("div",element_id,"width",element.offsetWidth);
	frappe.model.set_value("div",element_id,"x",element.style.left.split('px')[0]);
	frappe.model.set_value("div",element_id,"y",element.style.top.split('px')[0]);
}
function save_header_elements(frm){
	frm.doc.header_elements.forEach(function(element){save_element(frm,element.name);console.log("saved"+element.name);  });
}








