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
            "fieldname": "item",
            "label": _("Item"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 80
        },
		{
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
        },
		{
            "fieldname": "nos",
            "label": _("No of Bags"),
            "fieldtype": "Int",
        },
		{
            "fieldname": "bag_weight",
            "label": _("Bag Weight"),
            "fieldtype": "Float",
        },
        {
            "fieldname": "total_weight",
            "label": _("Total Weight"),
            "fieldtype": "Float",
        },
        {
            "fieldname": "punching_die",
            "label": _("Punching Die"),
            "fieldtype": "Link",
			"options": "Punching Die"
        },
		{
            "fieldname": "brand",
            "label": _("Brand"),
            "fieldtype": "Link",
            "options": "Brand",
            "width": 80
        },
		{
            "fieldname": "coated",
            "label": _("Coated"),
            "fieldtype": "Check",
        },
        {
            "fieldname": "printed",
            "label": _("Printed"),
            "fieldtype": "Check"
        },
		{
            "fieldname": "warehouse",
            "label": _("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 100
        },
    ]

def get_data(filters=None):
	conditions = ""

	if filters.status:
		conditions += " and bag.status = '{0}' ".format(filters.status)

	if filters.item:
		conditions += " and bag.item = '{0}' ".format(filters.item)
	
	if filters.brand:
		conditions += " and bag.brand = '{0}' ".format(filters.brand)

	return frappe.db.sql("""
		select 
			bag.item as "Item:Link/Item:150", 
			bag.status, 
			count(bag.item), 
			bag.weight,
			sum(bag.weight),
			bag.punching_die, 
			bag.brand, 
			bag.coated_reel, 
			bag.printed_reel, 
			bag.warehouse       
		
		from 
			`tabPNI Bag` as bag
			
		where 
			docstatus = "1" {0}
			
		group by 
			bag.item, bag.coated_reel, bag.printed_reel, bag.warehouse, bag.weight;
    """.format(conditions))