// Copyright (c) 2021, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Custom Print Format', {
	qr_code_color:function(frm){
	if (frm.doc.qr_code_type=="text"){
	document.getElementById("qr_code").src = "https://api.qrserver.com/v1/create-qr-code/?size=160x160&color="+frm.doc.qr_code_color.substring(1)+"&data=test";
}}
});
frappe.ui.form.on('Custom Print Format', {
        qr_code_type:function(frm){place_qr_code(frm);}
});


frappe.ui.form.on('Custom Print Format', {
	 refresh: function(frm) {



frappe.call({
                                        method : "slnee.data.get_fields",
                                        args:{
                                                "doctype":"Sales Invoice"
                                            },
                                        callback(r) {
                                                if(r.message){}
                                                }
                                        });

var sidebar= document.getElementsByClassName("layout-side-section")[0]; 
var element = document.createElement("div");
element.setAttribute("id","utils");
element.style.wisth="100%;"
var el1=document.createElement("div");
el1.innerHTML="<i class='fa fa-trash' style='font-size:22px;color:gray;'></i>";
element.appendChild(el1);
sidebar.appendChild(element);





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
	save_body_elements(frm);
	save_qr_code(frm);
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

});

function head_elements(frm){
frm.doc.elements.forEach(function(element){

});

}

function place(element,parent_id,frm){
	if (element.disabled == 0) {
		var parent = document.getElementById(parent_id);
		if (element.type == "Label"){ //label
			var element_ = document.createElement("div");
			add_css(frm,".text_element{touch-action:none;}");
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
			if (element.underline ==1){
				element_.style.textDecoration = "underline";
						}
			var text = element.label;
			if (element.italic){text=text.italics()}
			if (element.bold){text=text.bold()}
			element_.style.fontSize= element.font_size.toString()+"px";
			element_.innerHTML=text;}

		else if (element.type=="Image"){	//image
			
			var element_ = document.createElement("div");
			var img = document.createElement("img");
			img.style.height="auto";
			img.style.width="auto";
			add_css(frm,".image_element{touch-action:none;}");
                        element_.classList.add("image_element");
			img.src = element.image;
			img.style.borderRadius = element.border_radius.toString()+"%";
                        img.style.borderStyle=element.border;
                        img.style.borderColor=element.border_color;

			element_.appendChild(img);
		}
			//common
			element_.style.top=element.y.toString()+"px";
                        element_.style.left=element.x.toString()+"px";
                        element_.setAttribute("data-x",element.x);
                        element_.setAttribute("data-y",element.y);
			element_.classList.add('resize-drag');
                        element_.style.position="absolute";
			element_.style.width=element.width.toString()+"px";
			element_.style.height=element.height.toString()+"px";
			element_.setAttribute("id",element.name);
			element_.onclick = function() {element_click(element_)};
                        parent.appendChild(element_);
	}
}


function place_qr_code(frm){
	if (document.getElementById("qr_code")!= undefined){
	document.getElementById("qr_code").remove();}
	if (frm.doc.qr_code_type=="text")
	{
		var parent = document.getElementById("bodyspace");
		var element_ = document.createElement("div");
		var img =  document.createElement("img");
		element_.setAttribute("id","qr_code");
                add_css(frm,".image_element{touch-action:none;}");
                element_.classList.add("image_element");
                img.src = "https://api.qrserver.com/v1/create-qr-code/?size=500x500&color="+frm.doc.qr_code_color.substring(1)+"&data=test";
		element_.classList.add('resize-drag');
                element_.style.position="absolute";
		element_.style.top=frm.doc.qr_code_y.toString()+"px";
                element_.style.left=frm.doc.qr_code_x.toString()+"px";
                element_.setAttribute("data-x",frm.doc.qr_code_x);
                element_.setAttribute("data-y",frm.doc.qr_code_y);
		element_.style.width=frm.doc.qr_code_width.toString()+"px";
                element_.style.height=frm.doc.qr_code_height.toString()+"px";
		element_.appendChild(img);
		parent.appendChild(element_);
}



}

function first_creation(frm){
	fix_header(frm);
	document.getElementById("headspace").innerHTML="";
	document.getElementById.onclick = function() {clear_select()};
	frm.doc.header_elements.forEach(function(element){
		place(element,"headspace",frm)
		});
	place_qr_code(frm)
	frm.doc.body_elements.forEach(function(element){
                place(element,"bodyspace",frm)
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
	if (old_css == undefined){old_css="";}
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
	if (element != undefined) {
	frappe.model.set_value("div",element_id,"height",element.offsetHeight);
	frappe.model.set_value("div",element_id,"width",element.offsetWidth);
	frappe.model.set_value("div",element_id,"x",element.style.left.split('px')[0]);
	frappe.model.set_value("div",element_id,"y",element.style.top.split('px')[0]);}
}

function save_qr_code(frm){
var element =  document.getElementById("qr_code");
        if (element != undefined) {
	frm.set_value("qr_code_x",element.style.left.split('px')[0]);
	frm.set_value("qr_code_y",element.style.top.split('px')[0]);
	if (element.offsetHeight>0){
	frm.set_value("qr_code_height",element.offsetHeight);}
	if (element.offsetWidth >0){
	frm.set_value("qr_code_width",element.offsetWidth);}
	refresh_field("qr_code_x");refresh_field("qr_code_y");refresh_field("qr_code_height");refresh_field("qr_code_width");

}

}



function set_labels(frm,element_id){
console.log(element_id);
		frappe.model.set_value("div",element_id,"doc_field","test");
}

function set_all_labels(frm){
frm.doc.header_elements.forEach(function(element){set_labels(frm,element.name);  });
}



function save_header_elements(frm){
	if (frm.doc.header_elements != undefined){
	frm.doc.header_elements.forEach(function(element){save_element(frm,element.name);  });
}}

function save_body_elements(frm){
        if (frm.doc.body_elements != undefined){
        frm.doc.body_elements.forEach(function(element){save_element(frm,element.name);  });
}}




function element_click(element){
//
//clear_select();
//if (element.style.borderStyle!="dashed"){
//element.style.borderStyle="dashed";
//element.style.borderColor="gray"
//}else{
//element.style.borderStyle="none";
//}
}

function clear_select(){
/*
var texts= document.getElementsByClassName("text_element");
for (var i =0; i<texts.length;i++){

texts[i].style.borderStyle="none";
}
var texts= document.getElementsByClassName("image_element");
for (var i =0; i<texts.length;i++){
texts[i].style.borderStyle="none";
}
*/

}




