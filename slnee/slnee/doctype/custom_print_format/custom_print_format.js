// Copyright (c) 2021, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Custom Print Format', {
	qr_code_color:function(frm){
	if (frm.doc.qr_code_type=="text"){
	document.getElementById("qr_code").src = "https://api.qrserver.com/v1/create-qr-code/?size=160x160&color="+frm.doc.qr_code_color.substring(1)+"&data=test";}}
});
frappe.ui.form.on('Custom Print Format', {
        qr_code_type:function(frm){place_qr_code(frm);}
});
frappe.ui.form.on('Custom Print Format', {
        show:function(frm){fix_header(frm);},
	border_color:function(frm){fix_header(frm);},
	border:function(frm){fix_header(frm);},
	//height:function(frm){fix_header(frm);};
	get_default_header:function(frm){
	frm.clear_table("header_elements");
	frm.refresh_field("header_elements");
	frappe.call({
		method:"frappe.client.get",
		args: {
			"doctype":"Company",
			"name":frm.doc.company
			},
		callback(r){
			if(r.message){
			let row = frm.add_child('header_elements',{
				label:r.message.name,
				color:r.message.color,
				type:"Label",
				width:270,
				height:frm.doc.height-12,
				x:6,
				y:6,
				font_size:25,
				text_align:"left"
			});
			let row2 = frm.add_child('header_elements',{ 
                                label:r.message.company_name_in_arabic,
                                color:r.message.color,
                                type:"Label",
				width:265,
				height:frm.doc.height-12,
				x:505,
				y:6,
				font_size:25,
				text_align:"right"

                        });
			let row3 = frm.add_child('header_elements',{ 
                                label:"Logo",
				image:r.message.company_logo,
				center:1,
                                //color:r.message.color,
                                type:"Image",
                                width:frm.doc.height-12,
                                height:frm.doc.height-12,
                                //x:220,
                                y:5,
                                //font_size:25

                        });


			frm.refresh_field("header_elements");
			fix_header(frm);
			}
		}
	});
}
});

frappe.ui.form.on('Custom Print Format', {
        show_footer:function(frm){fix_footer(frm);},
	footer_border_color:function(frm){fix_footer(frm);},
	footer_border:function(frm){fix_footer(frm);},
	//footer_height:function(frm){fix_footer(frm);}
});


frappe.ui.form.on('Custom Print Format', {
	 refresh: function(frm) {
document.getElementById("delete").onclick = function(){delete_element(frm);}
document.getElementById("disable").onclick = function(){disable_element(frm);}
document.getElementById("duplicate").onclick = function(){duplicate_element(frm);}
document.getElementById("bodyspace").onclick = function(){hideMenu();}
document.getElementById("headspace").onclick = function(){hideMenu();}
document.getElementById("page-Custom Print Format").onclick = function(){hideMenu();}
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
		frm.set_value("html",cont.innerHTML.replaceAll("dashed none","none"));
		frm.set_value("html",cont.innerHTML.replaceAll("none dashed","none"));
                refresh_field("html");
		save_header_elements(frm);
		save_body_elements(frm);
		save_qr_code(frm);
		save_footer_elements(frm);

},
after_save: function(frm){
frm.reload_doc();
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
			document.getElementById("headspace").style.height=frm.doc.height.toString()+"px";}

	}
});

//trigger when label change in a div
frappe.ui.form.on('div','label' ,function(frm,cdt,cdn){
	var div = locals[cdt][cdn];
	document.getElementById(div.name).innerHTML=div.label;
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
			element_.style.textAlign=element.text_align;
			element_.classList.add("btn-open-row");
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
			//if (element.italic){text=text.italics()}
			if (element.bold){element_.style.fontWeight="bold";}
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
		else if (element.type=="Table"){
			if (element.table_type=="Static"){
			//static table goes here
			var table = document.createElement("TABLE");
		
			}
		}
			//common
		var x= element.x;
		if (element.center ==1){
			x= 396-(element.width/2);
			}
		element_.style.top=element.y.toString()+"px";
                element_.style.left=x.toString()+"px";
                element_.setAttribute("data-x",x);
                element_.setAttribute("data-y",element.y);
		element_.classList.add('resize-drag');
		element_.classList.add('clickable001');
                element_.style.position="absolute";
		element_.style.width=element.width.toString()+"px";
		element_.style.height=element.height.toString()+"px";
		element_.setAttribute("id",element.name);
		element_.onclick = function() {element_click(element_);hideMenu();};
		element_.oncontextmenu = rightClick;
                parent.appendChild(element_);
	}
}
function hideMenu() {
            document.getElementById(
                "contextMenu").style.display = "none"
        }
  
function rightClick(e) {
            e.preventDefault();
            if (document.getElementById(
                "contextMenu").style.display == "block")
                hideMenu();
            
		var parent_id = this.parentElement.id;
                var menu = document.getElementById("contextMenu")
		menu.children[0].setAttribute("id",parent_id+"%%"+this.id);
                menu.style.display = 'block';
		//remove delete -duplicate if it's qr code
		if (this.id=="qr_code")
			{
			document.getElementById("del").style.display="none";
			document.getElementById("dup").style.display="none";}
		//retrieve delete - duplicate if it's not
		else{
			 document.getElementById("del").style.display="block";
			 document.getElementById("dup").style.display="block";}
		//if the element is too right, make the menu on left
		if (this.offsetLeft+this.offsetWidth > 600)
			{ menu.style.left = (this.offsetLeft-150).toString()+"px";}
		else //menu on right 
			{menu.style.left = (this.offsetLeft+this.offsetWidth).toString()+"px";}
		if (parent_id=="headspace"){
                menu.style.top = this.style.top;}
		if (parent_id=="bodyspace"){
			menu.style.top= (this.offsetTop+ document.getElementById("headspace").offsetHeight).toString()+"px";}
		if (parent_id=="footspace"){
                        menu.style.top= (this.offsetTop+ document.getElementById("headspace").offsetHeight + document.getElementById("bodyspace").offsetHeight).toString()+"px";}


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
		var text = frm.qr_code_text;
		if(text == undefined){text="write your text inside the specified box."}
                img.src = "https://api.qrserver.com/v1/create-qr-code/?size=500x500&color="+frm.doc.qr_code_color.substring(1)+"&data="+text.replaceAll("\n","%0A");
		element_.classList.add('resize-drag');
                element_.style.position="absolute";
		element_.style.top=frm.doc.qr_code_y.toString()+"px";
                element_.style.left=frm.doc.qr_code_x.toString()+"px";
                element_.setAttribute("data-x",frm.doc.qr_code_x);
                element_.setAttribute("data-y",frm.doc.qr_code_y);
		element_.style.width=frm.doc.qr_code_width.toString()+"px";
                element_.style.height=frm.doc.qr_code_height.toString()+"px";
		element_.appendChild(img);
		element_.onclick = function() {element_click(element_);hideMenu();};
                element_.oncontextmenu = rightClick;
		parent.appendChild(element_);
}




}

function first_creation(frm){
	document.getElementById.onclick = function() {clear_select()};
	
	place_qr_code(frm)
	frm.doc.body_elements.forEach(function(element){
                place(element,"bodyspace",frm)
                });
	place_qr_code(frm)
	fix_header(frm);
        fix_footer(frm);

}


function fix_header(frm){
	document.getElementById("headspace").innerHTML="";
	if (frm.doc.show != "No"){
		var header =  document.getElementById("headspace");
		header.style.display="block";
		header.style.borderColor=frm.doc.border_color;
		header.style.borderStyle=frm.doc.border;
		header.style.borderWidth=frm.doc.header_border_width.toString()+"px";
		header.style.height=frm.doc.height.toString()+"px";
		if (frm.doc.border=="none"){
			header.style.borderBottom="dashed 1px #CCC";
		}

		if (frm.doc.show =="Yes"){
        frm.doc.header_elements.forEach(function(element){
                place(element,"headspace",frm)
                });}

				}
	else{var header =  document.getElementById("headspace");
                header.style.display="none";}
}
function fix_footer(frm){
	document.getElementById("footspace").innerHTML="";
        if (frm.doc.show_footer != "No"){
                var footer =  document.getElementById("footspace");
                footer.style.display="block";
                footer.style.borderColor=frm.doc.footer_border_color;
                footer.style.borderStyle=frm.doc.footer_border;
		footer.style.borderWidth=frm.doc.footer_border_width.toString()+"px";
                footer.style.height=frm.doc.footer_height.toString()+"px";
		if (frm.doc.footer_border=="none"){
                        footer.style.borderTop="dashed 1px #CCC";
                }


if (frm.doc.show_footer =="Yes"){
        frm.doc.footer_elements.forEach(function(element){
                place(element,"footspace",frm)
                });}

                                }
        else{var footer =  document.getElementById("footspace");
                footer.style.display="none";}
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
function clear_css_links(frm){
	frm.set_value("css","");
	frm.set_value("links","");
	refresh_field("links");
	refresh_field("css");
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
		frappe.model.set_value("div",element_id,"doc_field","test");
}

function set_all_labels(frm){
frm.doc.header_elements.forEach(function(element){set_labels(frm,element.name);  });
}



function save_header_elements(frm){
	if (frm.doc.header_elements != undefined){
	frm.doc.header_elements.forEach(function(element){save_element(frm,element.name);  });
}}

function save_footer_elements(frm){
        if (frm.doc.footer_elements != undefined){
        frm.doc.footer_elements.forEach(function(element){save_element(frm,element.name);  });
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



function delete_element(frm){
	var element = document.getElementById("delete").parentElement.parentElement.id.split('%%');
	var table= element[0];
	var row_name=element[1];
	console.log(table,row_name);
	remove_row(frm,table,row_name);
	document.getElementById(row_name).remove();
	hideMenu();
}

function disable_element(frm){
	var element = document.getElementById("delete").parentElement.parentElement.id.split('%%');
        var table= element[0];
        var row_name=element[1];
	if (row_name=="qr_code"){
		frm.set_value("qr_code_type","none");
		frm.refresh_field("qr_code_type");
		document.getElementById("qr_code").remove();
		hideMenu();
	}
	else{
	disable_row(frm,table,row_name);
        document.getElementById(row_name).remove();
        hideMenu();

}
}

function duplicate_element(frm){
	var element = document.getElementById("delete").parentElement.parentElement.id.split('%%');
        var table= element[0];
        var row_name=element[1];
	duplicate_row(frm,table,row_name);
	



}

function remove_row(frm,table,row_name){
	if (table=="headspace"){table="header_elements";var i= frm.doc.header_elements.length;}
	else if (table=="footspace"){table="footer_elements";var i = frm.doc.footer_elements.length;}
	else {table="body_elements";var i=frm.doc.body_elements.length;}
		while (i--)
		{
    			if(frm.doc[table][i].name==row_name)
    			{
        			frm.get_field(table).grid.grid_rows[i].remove();
    			}
		}
	frm.refresh_field(table);
}


function disable_row(frm,table,row_name){
	frappe.model.set_value("div",row_name,"disabled",1)
	if (table=="headspace"){table="header_elements";}
        else if (table=="footspace"){table="footer_elements";}
        else {table="body_elements";}
	frm.refresh_field(table);

}


function duplicate_row(frm,table,row_name){
	if (table=="headspace"){var parent="header_elements";}
        else if (table=="footspace"){var parent="footer_elements";}
        else {var parent="body_elements";}

	var doc = frappe.model.get_doc("div",row_name);
	if (doc.image==undefined){
		var img="";
	}else {var img=doc.image;}
	if (doc.font==undefined){
		var font="";}
	else {var font = doc.font;}
	let row = frm.add_child(parent,{
                                label:doc.label,
                                color:doc.color,
                                type:doc.type,
				image:img,
                                width:doc.width,
                                height:doc.height,
                                x:6,
                                y:6,
                                font_size:doc.font_size,
                                text_align:doc.text_align,
				font:font,
				//border:doc.border,
				//border_color:doc.border_color;
				bold:doc.bold,
				underline:doc.underline,
				italic:doc.italic,
				center:0,
				//border_radius:doc.border_radius
                        });
	place(row,table,frm);
	frm.refresh_field(parent);

}
