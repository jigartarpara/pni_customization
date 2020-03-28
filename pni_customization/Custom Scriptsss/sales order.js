frappe.ui.form.on('Sales Order', {
	is_order_approved_by_customer(frm) {
	    if(frm.doc.is_order_approved_by_customer === 1){
	        frm.set_value("image","");
	        frm.set_df_property('image','reqd', 1);
	    }
	    if(frm.doc.is_order_approved_by_customer === 0){
	        frm.set_value("image","");
	        frm.set_df_property('image','reqd', 0);
	    }
	}
});

frappe.ui.form.on("Sales Order Item",{
	"item_code" : function (frm, cdt, cdn){
		cur_frm.clear_table("last_customer_sales_table");
		var d2 = locals[cdt][cdn];
		if(frm.doc.customer && d2.item_code){
			frappe.call({
				"method": "last_records.last_records.doctype.last_purchase_table.last_purchase_table.getLastSalesprice",
				args: {
					item_code: d2.item_code,
				},
				callback:function(r){
					var len=r.message.length;
					for (var i=0;i<len;i++){  
						var row = frm.add_child("last_customer_sales_table");
						row.invoice_number = r.message[i][0];
						row.customer = r.message[i][1];
						row.invoice_date = r.message[i][2];
						row.item_code = r.message[i][3];
						row.qty = r.message[i][4];
						row.rate = r.message[i][5];
					}
				}
			});
		}
	}
});
                	
frappe.ui.form.on("Sales Order Item",{
	"item_code" : function (frm, cdt, cdn){
		cur_frm.clear_table("last_sales_table");
		var d2 = locals[cdt][cdn];
		if(d2.item_code){
			frappe.call({
				"method": "last_records.last_records.doctype.last_purchase_table.last_purchase_table.getLastSalespriceCustomer",
				args: {
					item_code: d2.item_code,
					customer : frm.doc.customer
				},
				callback:function(r){
					var len=r.message.length;
					for (var i=0;i<len;i++){  
						var row = frm.add_child("last_sales_table");
							row.invoice_number = r.message[i][0];
							row.invoice_date = r.message[i][1];
							row.item_code = r.message[i][2];
							row.qty = r.message[i][3];
							row.rate = r.message[i][4];
					}
				}
			});
		}
		d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
	},
	"uom": function(frm, cdt,cdn){
		var d2 = locals[cdt][cdn];
		d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
	},
	"qty": function(frm, cdt, cdn){
		var d2 = locals[cdt][cdn];
		d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
		frm.refresh_field("items")
	},
	"base_uom_rate": function(frm, cdt, cdn){
		var d2 = locals[cdt][cdn];
		if(parseFloat(d2.base_uom_rate * d2.conversion_factor) < d2.price_list_rate){
			frappe.msgprint("Rate can't be less then "+parseFloat(d2.price_list_rate / d2.conversion_factor	))
			d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
			frm.refresh_field("items")
			return;
		}
		d2.rate = parseFloat(d2.base_uom_rate * d2.conversion_factor)
		frm.refresh_field("items")
	},
	"rate": function(frm, cdt, cdn){
		var d2 = locals[cdt][cdn];
		if(d2.rate < d2.price_list_rate){
			frappe.msgprint("Rate can't be less then "+d2.price_list_rate)
			d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
			frm.refresh_field("items")
		}
	}
});

function showPosition(position){
	frm.set_value("latitude",position.coords.latitude);
	frm.set_value("longitude",position.coords.longitude);
}
       	
frappe.ui.form.on('Sales Order', {
	onload(frm) {
	    if(frm.doc.docstatus === 0){
			navigator.geolocation.getCurrentPosition(showPosition);
			
	    }
	}
});


frappe.ui.form.on("Sales Order", "google_map", function(frm) {
   window.open("http://www.google.com/maps/place/" + frm.doc.latitude + "," + frm.doc.longitude);
});