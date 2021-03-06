# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime, time_diff_in_hours, flt

class Punching(Document):
	def validate(self):
		self.manage_table()
		if self.end_dt and self.start_dt:
			hours = time_diff_in_hours(self.end_dt, self.start_dt)
			frappe.db.set(self, 'operation_hours', hours)

	def onload(self):
		paper_blank_setting = frappe.get_doc("Paper Blank Settings","Paper Blank Settings")
		self.set_onload("scrapitemgroup", paper_blank_setting.punching_scrap)

	def manage_table(self):
		# setting = frappe.get_doc("PNI Settings","PNI Settings")
		for data in self.punching_table:
			reel_in = frappe.get_doc("Reel",data.reel_in)
			if not data.half_reel:
				"""
					In case of no half reel
					create table and 
					delete reel out if creted
				"""
				if data.reel_out:
					frappe.msgprint("Please Manually Delete Reel "+data.reel_out)
					data.reel_out = ""
				if not data.punch_table:
					doc = frappe.get_doc({
						"doctype": "Punch Table",
						"status": "Draft"
					})
					doc.insert()
					data.punch_table = doc.name
				else:
					doc = frappe.get_doc("Punch Table",data.punch_table)
				doc.custom_id = data.custom_id
				doc.item = data.item_out
				doc.printed_item = reel_in.printed_item
				doc.supplier_reel_id = reel_in.supplier_reel_id
				doc.punching_die = data.punching_die
				doc.brand = reel_in.brand
				doc.coated_reel = reel_in.coated_reel
				doc.printed_reel = reel_in.printed_reel
				doc.weight = data.weight_out
				doc.punching_die = data.punching_die
				doc.save()
			else:
				"""
					In Case of Hallf Reel Don;t 
					Create table 
					need to create table
					and delete table if created
				"""
				if data.punch_table:
					frappe.msgprint("Please Manually Delete Table "+data.punch_table)
					data.punch_table = ""
				if not data.reel_out:
					doc = frappe.get_doc({
						"doctype": "Reel",
						"status": "Draft",
						"process_prefix": "PN",
						"posting_date": self.date
					})
					doc.insert()
					data.reel_out = doc.name
				else:
					doc = frappe.get_doc("Reel",data.reel_out)
				
				doc.custom_id = data.custom_id
				doc.supplier_reel_id = reel_in.supplier_reel_id
				doc.item = data.item_out if not data.half_reel else reel_in.item
				doc.printed_item = reel_in.printed_item
				doc.warehouse = self.fg_warehouse if not data.half_reel else self.src_warehouse
				doc.type = reel_in.type
				doc.brand = reel_in.brand
				doc.blank_weight = reel_in.blank_weight
				doc.coated_reel =  reel_in.coated_reel
				doc.printed_reel = reel_in.printed_reel
				doc.printed_weight = reel_in.printed_weight
				doc.coated_weight = reel_in.coated_weight
				doc.weight = data.weight_out
				doc.type = reel_in.type
				if data.half_reel:
					doc.item = reel_in.item
					doc.warehouse = self.src_warehouse
				doc.save()
	
	def manage_reel_tracking(self):
		for data in self.punching_table:
			doc = frappe.get_doc({
				"doctype": "Reel Tracking",
				"status": "Draft",
				"reel": data.reel_in,
				"reel_process": "Punching",
				"date": frappe.utils.nowdate(),
				"time": frappe.utils.nowtime(),
				"out_reel": data.punch_table,
				"status": "Punching Submit",
				"process_reference": self.name
			})
			doc.insert(ignore_permissions=True)
	
	def cancel_reel_tracking(self):
		for data in self.punching_table:
			doc = frappe.get_doc({
				"doctype": "Reel Tracking",
				"status": "Draft",
				"reel": data.reel_in,
				"reel_process": "Punching",
				"date": frappe.utils.nowdate(),
				"time": frappe.utils.nowtime(),
				"out_reel": data.punch_table,
				"status": "Punching Cancel",
				"process_reference": self.name
			})
			doc.insert(ignore_permissions=True)

	def on_submit(self):
		# if (not self.end_dt) or (not self.end_dt):
		# 	frappe.throw("Please Select Operation Start and End Time")
		for item in self.punching_table:
			if ((not item.reel_in) or (not item.punch_table)) and not item.half_reel:
				frappe.throw("Reel  and Punch Table is Compulsory")
		for data in self.punching_table:
			if not data.weight_out:
				frappe.throw("Weight Can't be empty")
			reel_in = frappe.get_doc("Reel",data.reel_in)
			reel_in.status = "Consume"
			reel_in.save()
			if not data.half_reel:
				punch_table = frappe.get_doc("Punch Table",data.punch_table)
				punch_table.status = "In Stock"
				punch_table.save()
				punch_table.submit()
			else:
				reel_out = frappe.get_doc("Reel",data.reel_out)
				reel_out.status = "In Stock"
				reel_out.save()
				reel_out.submit()

		self.manage_reel_tracking()
		frappe.db.set(self, 'status', 'Pending For Stock Entry')
	
	def on_cancel(self):
		stock_entry = frappe.db.sql("""select name from `tabStock Entry`
			where pni_reference = %s and docstatus = 1""", self.name)
		if stock_entry:
			frappe.throw(_("Cannot cancel because submitted Stock Entry \
			{0} exists").format(stock_entry[0][0]))
		frappe.db.set(self, 'status', 'Cancelled')
		for data in self.punching_table:
			reel_in = frappe.get_doc("Reel",data.reel_in)
			reel_in.status = "In Stock"
			reel_in.save()
			punch_table = frappe.get_doc("Punch Table",data.punch_table)
			punch_table.cancel()
		self.cancel_reel_tracking()
	def get_debug(self):
		qty_of_total_production = operating_cost = raw_material_cost = 0
		
		for item in self.punching_table:
			if item.weight_out > 0:
				qty_of_total_production = float(qty_of_total_production) + item.weight_out
				raw_material_cost += self.get_valuation_rate(item.item) * float(item.weight)

		production_cost = raw_material_cost + operating_cost
		frappe.errprint("qty_of_total_production")
		frappe.errprint(qty_of_total_production)
		frappe.errprint("production_cost")
		frappe.errprint(production_cost)
		return 
	def manufacture_entry(self):
		return self.make_stock_entry()
	
	def make_stock_entry(self):
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.pni_reference_type = "Punching"
		stock_entry.pni_reference = self.name
		stock_entry.pni_shift = self.shift_time
		stock_entry.posting_date = self.date
		stock_entry.set_posting_time = True
		
		stock_entry.stock_entry_type = "Manufacture"
		stock_entry = self.set_se_items_finish(stock_entry)
		return stock_entry.as_dict()
	
	def get_valuation_rate(self, item):
		""" Get weighted average of valuation rate from all warehouses """

		total_qty, total_value, valuation_rate = 0.0, 0.0, 0.0
		for d in frappe.db.sql("""select actual_qty, stock_value from `tabBin`
			where item_code=%s""", item, as_dict=1):
				total_qty += flt(d.actual_qty)
				total_value += flt(d.stock_value)

		if total_qty:
			valuation_rate =  total_value / total_qty

		if valuation_rate <= 0:
			last_valuation_rate = frappe.db.sql("""select valuation_rate
				from `tabStock Ledger Entry`
				where item_code = %s and valuation_rate > 0
				order by posting_date desc, posting_time desc, creation desc limit 1""", item)

			valuation_rate = flt(last_valuation_rate[0][0]) if last_valuation_rate else 0

		if not valuation_rate:
			valuation_rate = frappe.db.get_value("Item", item, "valuation_rate")

		return flt(valuation_rate)
	
	def set_se_items_finish(self, se):
		se.from_warehouse = self.src_warehouse
		se.to_warehouse = self.fg_warehouse

		raw_material_cost = 0
		operating_cost = 0
		reelin = []
		for item in self.punching_table:
			if item.reel_in not in reelin:
				se = self.set_se_items(se, item, se.from_warehouse, None, False, reel_in= True)
				reelin.append(item.reel_in)
				raw_material_cost += self.get_valuation_rate(item.item) * float(item.weight)		

		qty_of_total_production = 0
		total_sale_value = 0
		for item in self.punching_table:
			if item.weight_out > 0:
				qty_of_total_production = float(qty_of_total_production) + item.weight_out
				

		production_cost = raw_material_cost + operating_cost

		#add Stock Entry Items for produced goods and scrap
		for item in self.punching_table:
			warehouse = se.to_warehouse if not item.half_reel else se.from_warehouse
			
			se = self.set_se_items(se, item, None, warehouse, True, qty_of_total_production, total_sale_value, production_cost, table_out = True)

		for item in self.punching_scrap:
			se = self.set_se_items(se, item, None, self.scrap_warehouse, False, scrap_item = True)

		return se
	
	def set_se_items(self, se, item, s_wh, t_wh, calc_basic_rate=False, qty_of_total_production=None, total_sale_value=None, production_cost=None, reel_in = False, table_out = False, scrap_item = False):
		item_from_reel = {}
		class Empty:
			pass  
		if reel_in:
			item_from_reel = frappe.get_doc("Reel",item.reel_in)
		if table_out:
			if not item.half_reel:
				item_from_reel = frappe.get_doc("Punch Table",item.punch_table)
			else:
				item_from_reel = frappe.get_doc("Reel",item.reel_out)
		if scrap_item:
			item_from_reel = Empty()
			item_from_reel.item = item.item
			item_from_reel.weight = item.qty

		expense_account, cost_center = frappe.db.get_values("Company", self.company, \
			["default_expense_account", "cost_center"])[0]
		item_name, stock_uom, description = frappe.db.get_values("Item", item_from_reel.item, \
			["item_name", "stock_uom", "description"])[0]

		item_expense_account, item_cost_center = frappe.db.get_value("Item Default", {'parent': item_from_reel.item, 'company': self.company},\
			["expense_account", "buying_cost_center"])

		if not expense_account and not item_expense_account:
			frappe.throw(_("Please update default Default Cost of Goods Sold Account for company {0}").format(self.company))

		if not cost_center and not item_cost_center:
			frappe.throw(_("Please update default Cost Center for company {0}").format(self.company))

		se_item = se.append("items")
		se_item.item_code = item_from_reel.item
		se_item.qty = item_from_reel.weight
		se_item.s_warehouse = s_wh
		se_item.t_warehouse = t_wh
		se_item.item_name = item_name
		se_item.description = description
		se_item.uom = stock_uom
		se_item.stock_uom = stock_uom

		se_item.expense_account = item_expense_account or expense_account
		se_item.cost_center = item_cost_center or cost_center

		# in stock uom
		se_item.transfer_qty = item_from_reel.weight
		se_item.conversion_factor = 1.00

		item_details = se.run_method( "get_item_details",args = (frappe._dict(
		{"item_code": item_from_reel.item, "company": self.company, "uom": stock_uom, 's_warehouse': s_wh})), for_update=True)

		for f in ("uom", "stock_uom", "description", "item_name", "expense_account",
		"cost_center", "conversion_factor"):
			se_item.set(f, item_details.get(f))

		if calc_basic_rate:
			print(item_from_reel.item)
			print(production_cost)
			print(qty_of_total_production)
			se_item.basic_rate = production_cost/qty_of_total_production
		if scrap_item:
			se_item.basic_rate = self.get_valuation_rate(item_from_reel.item)
		return se

