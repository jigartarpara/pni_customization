# Copyright (c) 2013, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    data = get_data(filters)
    columns = get_columns()
    return columns, data

def get_columns():
    return  [
        {
            "fieldname": "workstation",
            "label": _("Workstation"),
            "fieldtype": "Link",
            "options": "Workstation",
            "width": 150
        },
		{
            "fieldname": "production",
            "label": _("Total Production"),
            "fieldtype": "Int",
        },
        {
            "fieldname": "scrap",
            "label": _("Total Scrap"),
            "fieldtype": "Float",
        },
		{
            "fieldname": "scrap_item",
            "label": _("Scrap Item"),
            "fieldtype": "Link",
			"options": "Item"
        }
    ]
def get_condition(filters):
    condition1,condition2  = "",""
    if filters.get("from_date"): condition1 += " AND packing.date >= %(from_date)s"
    if filters.get("from_date"): condition2 += " AND stock_entry.posting_date >= %(from_date)s"
    if filters.get("to_date"): condition1 += " AND packing.date <= %(to_date)s"
    if filters.get("to_date"): condition2 += " AND stock_entry.posting_date <= %(to_date)s"
    return condition1,condition2

def get_data(filters=None):
	condition1,condition2 = get_condition(filters)

	return frappe.db.sql("""
		select table1.workstation,table1.total_production,table2.total_scrap, table2.item_code
			from 
				
				(select 
					packing.workstation as workstation, sum(pni_crt.total) as total_production 
				from 
					`tabPNI Carton` as pni_crt,
					`tabPNI Packing` as packing, 
					`tabPNI Packing Carton` as pni_crt_tbl
					
				where 
					pni_crt.name = pni_crt_tbl.carton_id and
					pni_crt_tbl.parent = packing.name and
					pni_crt.docstatus = "1" and
					packing.docstatus = "1"
					%s
				group by packing.workstation) as table1,
				
				(select 
					stock_entry.pni_reference as workstation,
					item_table.item_code as item_code,
					sum(item_table.qty) as total_scrap 
				from 
					`tabStock Entry Detail` as item_table,
					`tabStock Entry` as stock_entry
				
				where
					item_table.parent = stock_entry.name and
					stock_entry.scrap_entry = "1" and
					stock_entry.pni_reference_type = "Workstation"
					%s
				group by stock_entry.pni_reference, item_table.item_code) as table2
			
			where table1.workstation = table2.workstation
			
    """%(condition1, condition2), filters)