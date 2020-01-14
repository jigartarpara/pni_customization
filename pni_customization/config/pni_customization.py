from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Engineering"),
			"items": [
				{
					"type": "doctype",
					"name": "BOM",
					"description": _("BOM")
				},
				{
					"type": "doctype",
					"name": "Work Order",
					"description": _("Work Order")
				},
				{
					"type": "doctype",
					"name": "Job Card",
					"description": _("Job Card")
				},
				{
					"type": "doctype",
					"name": "Workstation",
					"description": _("Workstation")
				},
				{
					"type": "doctype",
					"name": "Operation",
					"description": _("Operation"),
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
					"description": _("Record item movement."),
				},
				{
					"type": "doctype",
					"name": "Item",
					"description": _("Items"),
				},
			]
		},
		{
			"label": _("Paper Cup Making"),
			"items": [
				{
					"type": "doctype",
					"name": "PNI Packing",
					"description": _("Detail of Paper Cup Carton"),
				},
				{
					"type": "doctype",
					"name": "Process Order",
					"description": _(" Record Production Detail")
				},
				{
					"type": "doctype",
					"name": "PNI Carton",
					"description": _("Carton Details"),
				},
				{
					"type": "doctype",
					"name": "Process Definition",
					"description": _("Process Definition."),
				},
				{
					"type": "doctype",
					"name": "Process Type",
					"description": _("Process Type."),
				},
                {
					"type": "doctype",
					"name": "Manufacturing Department",
					"description": _("Manufacturing Department"),
				},
                {
					"type": "doctype",
					"name": "Item",
					"description": _("All Products or Services."),
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
					"description": _("Record item movement."),
				}
			]
		},
		{
			"label": _("Paper Cup Reports"),
			"items": [
                {
					"type": "report",
					"name": "PNI Carton Stock",
					"is_query_report": True,
					"description": _("Initial Order From Customer"),
					"reference_doctype": "PNI Carton",
				}
			]
		},
		{
			"label": _("Paper Blank Processing"),
			"items": [
				{
					"type": "doctype",
					"name": "Coating",
					"description": _("Coating Details"),
				},
				{
					"type": "doctype",
					"name": "Slitting",
					"description": _("Slitting Details"),
				},
				{
					"type": "doctype",
					"name": "Printing",
					"description": _("Printing Details"),
				},
				{
					"type": "doctype",
					"name": "Printing Cylinder",
					"description": _("Printing Cylinder Master")
				},
				{
					"type": "doctype",
					"name": "Punching",
					"description": _("Punching Master")
				},
				{
					"type": "doctype",
					"name": "Punch Table",
					"description": _("Punched Table Master")
				},
				{
					"type": "doctype",
					"name": "Punching Die",
					"description": _("Punching Die Master")
				},
				{
					"type": "doctype",
					"name": "Reel",
					"description": _("Reel Master")
				},
				{
					"type": "doctype",
					"name": "Reel Tracking",
					"description": _("Reel History Tracking")
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
					"description": _("Record item movement."),
				}
			]
		},
		{
			"label": _("Sales"),
			"items": [
				{
					"type": "doctype",
					"name": "Lead",
					"description": _("Description")
				},
				{
					"type": "doctype",
					"name": "Opportunity",
					"description": _("Opportunity")
				},
				{
					"type": "doctype",
					"name": "PNI Quotation",
					"description": _("PNI Quotation")
				},
				{
					"type": "doctype",
					"name": "PNI Sales Order",
					"description": _("Initial Order From Customer"),
				},
				{
					"type": "doctype",
					"name": "Sales Order",
					"description": _("ERPNext Sales Order"),
				}
			]
		},
		
		{
			"label": _("Office Use"),
			"items": [
                {
					"type": "doctype",
					"name": "PNI Gate Entry",
					"description": _("Initial Order From Customer"),
				},
				{
					"type": "doctype",
					"name": "PNI Gate Pass",
					"description": _("Initial Order From Customer"),
				}
			]
		}
	]
