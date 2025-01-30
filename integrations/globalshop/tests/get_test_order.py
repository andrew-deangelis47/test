import json


def get_test_order_json() -> dict:
    """
    Get a test order as a JSON dict
    """

    json_str = """
{
"billing_info": null,
"created": "2021-10-12T18:39:36+00:00",
"contact": {
"account": {
"erp_code": "KNI002",
"id": 126343,
"metrics": {
"order_revenue_all_time": 15600.8,
"order_revenue_last_thirty_days": 15505.2,
"quotes_sent_all_time": 7,
"quotes_sent_last_thirty_days": 6
},
"notes": null,
"name": "Waffle Dreams",
"payment_terms": "Net 30",
"payment_terms_period": 30
},
"email": "jonathan.grose+gss@paperlessparts.com",
"first_name": "Jon",
"id": 196926,
"last_name": "Grose",
"notes": "",
"phone": "",
"phone_ext": ""
},
"customer": {
"id": null,
"company": {
"business_name": "Waffle Dreams",
"erp_code": "WD0001",
"id": null,
"metrics": {
"order_revenue_all_time": 15600.8,
"order_revenue_last_thirty_days": 15505.2,
"quotes_sent_all_time": 7,
"quotes_sent_last_thirty_days": 6
},
"notes": null,
"phone": "",
"phone_ext": ""
},
"email": "jonathan.grose+gss@paperlessparts.com",
"first_name": "Jon",
"last_name": "Grose",
"notes": "",
"phone": "",
"phone_ext": ""
},
"deliver_by": null,
"estimator": null,
"erp_code": null,
"number": 10,
"order_items": [
{
"id": 162662,
"components": [
{
"id": 1185154,
"child_ids": [],
"children": [],
"description": "BASE PLATE",
"export_controlled": false,
"finishes": [],
"innate_quantity": 1,
"is_root_component": false,
"material": {
"id": 56691,
"display_name": null,
"family": "Carbon Steel",
"material_class": "Metal",
"name": "Carbon Steel A36"
},
"material_operations": [
{
"id": 6170633,
"category": "material",
"cost": "178.89",
"costing_variables": [
{
"label": "Part Length (in)",
"variable_class": "basic",
"value_type": "number",
"value": 32.925,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Width (in)",
"variable_class": "basic",
"value_type": "number",
"value": 26.75,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Thickness (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.135,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Webbing (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.35,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Selection",
"variable_class": "table",
"value_type": "string",
"value": "MS10G60X120",
"row": {
"PART": "MS10G60X120",
"WIDTH": 60.0,
"LENGTH": 120.0,
"AMT_COST": 214.6714,
"THICKNESS": 0.135,
"row_number": 115,
"DESCRIPTION": "10 Ga. HRPO 60x120",
"PRODUCT_LINE": "RM",
"UM_INVENTORY": "EA"
},
"options": null,
"type": "table"
},
{
"label": "Material Description",
"variable_class": "basic",
"value_type": "string",
"value": "10 Ga. HRPO 60x120",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Sheet Length (in)",
"variable_class": "basic",
"value_type": "number",
"value": 120.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Width (in)",
"variable_class": "basic",
"value_type": "number",
"value": 60.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Thickness (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.135,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Sheet",
"variable_class": "basic",
"value_type": "number",
"value": 6.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Weight",
"variable_class": "basic",
"value_type": "number",
"value": 275.659,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Gross Weight",
"variable_class": "basic",
"value_type": "number",
"value": 45.943,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Net Weight",
"variable_class": "basic",
"value_type": "number",
"value": 11.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Cost Per Sheet",
"variable_class": "basic",
"value_type": "currency",
"value": 214.6714,
"row": null,
"options": null,
"type": "currency"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Material | 10 Ga. HRPO 60x120",
"operation_definition_name": "Sheet | Material",
"notes": null,
"quantities": [
{
"price": "35.78",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "178.89",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "357.79",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "715.57",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 1,
"runtime": null,
"setup_time": null
}
],
"parent_ids": [
1185146
],
"part_custom_attrs": [],
"part_name": "57-007-00002-N-3.step",
"part_number": "57-007-00002-N-3",
"part_url": "Test.url",
"part_uuid": "456a5c6d-96f8-40cb-aa80-83a58472b791",
"process": {
"id": 7563,
"external_name": "Sheet Metal",
"name": "Laser Only"
},
"purchased_component": null,
"revision": null,
"shop_operations": [
{
"id": 6170634,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "ENG",
"operation_definition_name": "ENG",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 2,
"runtime": null,
"setup_time": null
},
{
"id": 6170635,
"category": "operation",
"cost": "14.07",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "LZGP",
"row": {
"WORKGROUP": "LZGP",
"WORKCENTER": "LSR2",
"row_number": 8,
"Description": "AMADA FOMII 3015 RI",
"BILLING_RATE": 90.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 90.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Thickness",
"variable_class": "basic",
"value_type": "number",
"value": 0.135,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Use Manual Laser Length",
"variable_class": "drop_down",
"value_type": "string",
"value": "No",
"row": null,
"options": [
"No",
"Yes"
],
"type": "string"
},
{
"label": "Cut Length",
"variable_class": "basic",
"value_type": "number",
"value": 119.35,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Pierce Count",
"variable_class": "basic",
"value_type": "number",
"value": 22.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Cut Rates",
"variable_class": "table",
"value_type": "number",
"value": 135.0,
"row": {
"cut_rate": 135.0,
"thickness": 0.1644,
"row_number": 51,
"pierce_time": 1.0,
"material_family": "Carbon Steel"
},
"options": null,
"type": "table"
},
{
"label": "Material Cut Rate",
"variable_class": "basic",
"value_type": "number",
"value": 135.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Mat Pierce Time",
"variable_class": "basic",
"value_type": "number",
"value": 1.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 47.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.02127659574468085,
"row": null,
"options": null,
"type": "number"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.05,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "LZGP | 119.35 Cut Inches",
"operation_definition_name": "LZGP",
"notes": null,
"quantities": [
{
"price": "6.41",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "14.07",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "23.65",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "42.80",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 3,
"runtime": 0.02127659574468085,
"setup_time": 0.05
},
{
"id": 6170636,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "FW",
"operation_definition_name": "FW",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 4,
"runtime": null,
"setup_time": null
},
{
"id": 6170637,
"category": "operation",
"cost": "65.61",
"costing_variables": [
{
"label": "Labor Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "OSP Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 25.0,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Total Markup",
"operation_definition_name": "Total Markup",
"notes": null,
"quantities": [
{
"price": "22.78",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "65.61",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "129.69",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "257.85",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 5,
"runtime": null,
"setup_time": null
}
],
"supporting_files": [],
"thumbnail_url": "Test.url",
"type": "manufactured",
"deliver_quantity": 5,
"make_quantity": 5
},
{
"id": 1185153,
"child_ids": [],
"children": [],
"description": "FLAT PLATE",
"export_controlled": false,
"finishes": [],
"innate_quantity": 1,
"is_root_component": false,
"material": {
"id": 56691,
"display_name": null,
"family": "Carbon Steel",
"material_class": "Metal",
"name": "Carbon Steel A36"
},
"material_operations": [
{
"id": 6170628,
"category": "material",
"cost": "2.29",
"costing_variables": [
{
"label": "Part Length (in)",
"variable_class": "basic",
"value_type": "number",
"value": 5.854,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Width (in)",
"variable_class": "basic",
"value_type": "number",
"value": 5.572,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Thickness (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.048,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Webbing (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.35,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Selection",
"variable_class": "table",
"value_type": "string",
"value": "MS18G60X120",
"row": {
"PART": "MS18G60X120",
"WIDTH": 60.0,
"LENGTH": 120.0,
"AMT_COST": 91.5884,
"THICKNESS": 0.05,
"row_number": 140,
"DESCRIPTION": "18 Ga. CRS 60x120",
"PRODUCT_LINE": "RM",
"UM_INVENTORY": "EA"
},
"options": null,
"type": "table"
},
{
"label": "Material Description",
"variable_class": "basic",
"value_type": "string",
"value": "18 Ga. CRS 60x120",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Sheet Length (in)",
"variable_class": "basic",
"value_type": "number",
"value": 120.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Width (in)",
"variable_class": "basic",
"value_type": "number",
"value": 60.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Thickness (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.05,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Sheet",
"variable_class": "basic",
"value_type": "number",
"value": 200.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Weight",
"variable_class": "basic",
"value_type": "number",
"value": 102.096,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Gross Weight",
"variable_class": "basic",
"value_type": "number",
"value": 0.51,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Net Weight",
"variable_class": "basic",
"value_type": "number",
"value": 0.379,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Cost Per Sheet",
"variable_class": "basic",
"value_type": "currency",
"value": 91.5884,
"row": null,
"options": null,
"type": "currency"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Material | 18 Ga. CRS 60x120",
"operation_definition_name": "Sheet | Material",
"notes": null,
"quantities": [
{
"price": "0.46",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "2.29",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "4.58",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "9.16",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 1,
"runtime": null,
"setup_time": null
}
],
"parent_ids": [
1185146
],
"part_custom_attrs": [],
"part_name": "57-007-00002-N-7.step",
"part_number": "57-007-00002-N-7",
"part_url": "Test.url",
"part_uuid": "809811c0-443a-488f-858e-e831663d6e7b",
"process": {
"id": 7563,
"external_name": "Sheet Metal",
"name": "Laser Only"
},
"purchased_component": null,
"revision": null,
"shop_operations": [
{
"id": 6170629,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "ENG",
"operation_definition_name": "ENG",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 2,
"runtime": null,
"setup_time": null
},
{
"id": 6170630,
"category": "operation",
"cost": "9.98",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "LZGP",
"row": {
"WORKGROUP": "LZGP",
"WORKCENTER": "LSR2",
"row_number": 8,
"Description": "AMADA FOMII 3015 RI",
"BILLING_RATE": 90.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 90.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Thickness",
"variable_class": "basic",
"value_type": "number",
"value": 0.048,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Use Manual Laser Length",
"variable_class": "drop_down",
"value_type": "string",
"value": "No",
"row": null,
"options": [
"No",
"Yes"
],
"type": "string"
},
{
"label": "Cut Length",
"variable_class": "basic",
"value_type": "number",
"value": 22.852,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Pierce Count",
"variable_class": "basic",
"value_type": "number",
"value": 1.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Cut Rates",
"variable_class": "table",
"value_type": "number",
"value": 200.0,
"row": {
"cut_rate": 200.0,
"thickness": 0.0538,
"row_number": 57,
"pierce_time": 1.0,
"material_family": "Carbon Steel"
},
"options": null,
"type": "table"
},
{
"label": "Material Cut Rate",
"variable_class": "basic",
"value_type": "number",
"value": 200.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Mat Pierce Time",
"variable_class": "basic",
"value_type": "number",
"value": 1.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 458.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.002183406113537118,
"row": null,
"options": null,
"type": "number"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.1,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "LZGP | 22.85 Cut Inches",
"operation_definition_name": "LZGP",
"notes": null,
"quantities": [
{
"price": "9.20",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "9.98",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "10.97",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "12.93",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 3,
"runtime": 0.002183406113537118,
"setup_time": 0.1
},
{
"id": 6170631,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "FW",
"operation_definition_name": "FW",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 4,
"runtime": null,
"setup_time": null
},
{
"id": 6170632,
"category": "operation",
"cost": "4.17",
"costing_variables": [
{
"label": "Labor Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "OSP Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 25.0,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Total Markup",
"operation_definition_name": "Total Markup",
"notes": null,
"quantities": [
{
"price": "5.21",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "4.17",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "5.29",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "7.51",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 5,
"runtime": null,
"setup_time": null
}
],
"supporting_files": [],
"thumbnail_url": "Test.url",
"type": "manufactured",
"deliver_quantity": 5,
"make_quantity": 5
},
{
"id": 1185152,
"child_ids": [],
"children": [],
"description": null,
"export_controlled": false,
"finishes": [],
"innate_quantity": 1,
"is_root_component": false,
"material": {
"id": 56691,
"display_name": null,
"family": "Carbon Steel",
"material_class": "Metal",
"name": "Carbon Steel A36"
},
"material_operations": [
{
"id": 6170623,
"category": "material",
"cost": "21.36",
"costing_variables": [
{
"label": "Part Length (in)",
"variable_class": "basic",
"value_type": "number",
"value": 28.47,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Width (in)",
"variable_class": "basic",
"value_type": "number",
"value": 8.101,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Thickness (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.075,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Webbing (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.35,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Selection",
"variable_class": "table",
"value_type": "string",
"value": "MS14G60X120",
"row": {
"PART": "MS14G60X120",
"WIDTH": 60.0,
"LENGTH": 120.0,
"AMT_COST": 119.6244,
"THICKNESS": 0.075,
"row_number": 131,
"DESCRIPTION": "14 Ga. HRPO 60x120",
"PRODUCT_LINE": "RM",
"UM_INVENTORY": "EA"
},
"options": null,
"type": "table"
},
{
"label": "Material Description",
"variable_class": "basic",
"value_type": "string",
"value": "14 Ga. HRPO 60x120",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Sheet Length (in)",
"variable_class": "basic",
"value_type": "number",
"value": 120.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Width (in)",
"variable_class": "basic",
"value_type": "number",
"value": 60.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Thickness (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.075,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Sheet",
"variable_class": "basic",
"value_type": "number",
"value": 28.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Weight",
"variable_class": "basic",
"value_type": "number",
"value": 153.144,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Gross Weight",
"variable_class": "basic",
"value_type": "number",
"value": 5.469,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Net Weight",
"variable_class": "basic",
"value_type": "number",
"value": 4.746,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Cost Per Sheet",
"variable_class": "basic",
"value_type": "currency",
"value": 119.6244,
"row": null,
"options": null,
"type": "currency"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Material | 14 Ga. HRPO 60x120",
"operation_definition_name": "Sheet | Material",
"notes": null,
"quantities": [
{
"price": "4.27",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "21.36",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "42.72",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "85.45",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 1,
"runtime": null,
"setup_time": null
}
],
"parent_ids": [
1185146
],
"part_custom_attrs": [],
"part_name": "57-007-00002-N-6.step",
"part_number": "57-007-00002-N-6",
"part_url": "https://s3-fips.us-gov-west-1.amazonaws.com/parts.app.digitalmfg",
"process": {
"id": 7563,
"external_name": "Sheet Metal",
"name": "Laser Only"
},
"purchased_component": null,
"revision": null,
"shop_operations": [
{
"id": 6170624,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "ENG",
"operation_definition_name": "ENG",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 2,
"runtime": null,
"setup_time": null
},
{
"id": 6170625,
"category": "operation",
"cost": "8.19",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "LZGP",
"row": {
"WORKGROUP": "LZGP",
"WORKCENTER": "LSR2",
"row_number": 8,
"Description": "AMADA FOMII 3015 RI",
"BILLING_RATE": 90.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 90.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Thickness",
"variable_class": "basic",
"value_type": "number",
"value": 0.075,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Use Manual Laser Length",
"variable_class": "drop_down",
"value_type": "string",
"value": "No",
"row": null,
"options": [
"No",
"Yes"
],
"type": "string"
},
{
"label": "Cut Length",
"variable_class": "basic",
"value_type": "number",
"value": 73.142,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Pierce Count",
"variable_class": "basic",
"value_type": "number",
"value": 1.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Cut Rates",
"variable_class": "table",
"value_type": "number",
"value": 155.0,
"row": {
"cut_rate": 155.0,
"thickness": 0.1046,
"row_number": 54,
"pierce_time": 1.0,
"material_family": "Carbon Steel"
},
"options": null,
"type": "table"
},
{
"label": "Material Cut Rate",
"variable_class": "basic",
"value_type": "number",
"value": 155.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Mat Pierce Time",
"variable_class": "basic",
"value_type": "number",
"value": 1.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 122.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.00819672131147541,
"row": null,
"options": null,
"type": "number"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.05,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "LZGP | 73.14 Cut Inches",
"operation_definition_name": "LZGP",
"notes": null,
"quantities": [
{
"price": "5.24",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "8.19",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "11.88",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "19.25",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 3,
"runtime": 0.00819672131147541,
"setup_time": 0.05
},
{
"id": 6170626,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "FW",
"operation_definition_name": "FW",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 4,
"runtime": null,
"setup_time": null
},
{
"id": 6170627,
"category": "operation",
"cost": "10.05",
"costing_variables": [
{
"label": "Labor Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "OSP Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 25.0,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Total Markup",
"operation_definition_name": "Total Markup",
"notes": null,
"quantities": [
{
"price": "5.14",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "10.05",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "18.56",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "35.60",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 5,
"runtime": null,
"setup_time": null
}
],
"supporting_files": [],
"thumbnail_url": "Test.url",
"type": "manufactured",
"deliver_quantity": 5,
"make_quantity": 5
},
{
"id": 1185151,
"child_ids": [],
"children": [],
"description": "FORMED SECTION",
"export_controlled": false,
"finishes": [],
"innate_quantity": 1,
"is_root_component": false,
"material": {
"id": 56691,
"display_name": null,
"family": "Carbon Steel",
"material_class": "Metal",
"name": "Carbon Steel A36"
},
"material_operations": [
{
"id": 6170616,
"category": "material",
"cost": "7.27",
"costing_variables": [
{
"label": "Part Length (in)",
"variable_class": "basic",
"value_type": "number",
"value": 12.78123,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Width (in)",
"variable_class": "basic",
"value_type": "number",
"value": 7.86284,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Thickness (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.048,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Webbing (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.35,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Selection",
"variable_class": "table",
"value_type": "string",
"value": "MS18G60X120",
"row": {
"PART": "MS18G60X120",
"WIDTH": 60.0,
"LENGTH": 120.0,
"AMT_COST": 91.5884,
"THICKNESS": 0.05,
"row_number": 140,
"DESCRIPTION": "18 Ga. CRS 60x120",
"PRODUCT_LINE": "RM",
"UM_INVENTORY": "EA"
},
"options": null,
"type": "table"
},
{
"label": "Material Description",
"variable_class": "basic",
"value_type": "string",
"value": "18 Ga. CRS 60x120",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Sheet Length (in)",
"variable_class": "basic",
"value_type": "number",
"value": 120.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Width (in)",
"variable_class": "basic",
"value_type": "number",
"value": 60.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Thickness (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.05,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Sheet",
"variable_class": "basic",
"value_type": "number",
"value": 63.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Weight",
"variable_class": "basic",
"value_type": "number",
"value": 102.096,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Gross Weight",
"variable_class": "basic",
"value_type": "number",
"value": 1.621,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Net Weight",
"variable_class": "basic",
"value_type": "number",
"value": 0.827,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Cost Per Sheet",
"variable_class": "basic",
"value_type": "currency",
"value": 91.5884,
"row": null,
"options": null,
"type": "currency"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Material | 18 Ga. CRS 60x120",
"operation_definition_name": "Sheet | Material",
"notes": null,
"quantities": [
{
"price": "1.45",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "7.27",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "14.54",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "29.08",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 1,
"runtime": null,
"setup_time": null
}
],
"parent_ids": [
1185146
],
"part_custom_attrs": [],
"part_name": "57-007-00002-N-4.step",
"part_number": "57-007-00002-N-4",
"part_url": "Test.url",
"process": {
"id": 7559,
"external_name": "Sheet Metal Fabrication",
"name": "Laser & Form"
},
"purchased_component": null,
"revision": null,
"shop_operations": [
{
"id": 6170617,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "ENG",
"operation_definition_name": "ENG",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 2,
"runtime": null,
"setup_time": null
},
{
"id": 6170618,
"category": "operation",
"cost": "0",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "PG-B",
"row": {
"Department": "",
"Workcenter": "PG-B",
"row_number": 16,
"Description": "BRAKE PROGRAMMING",
"Billing_Rate": 32.0,
"Hours_per_Week": 40.0,
"Schedule_Percent_Modifier": 1.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 32.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Hours Per Week",
"variable_class": "basic",
"value_type": "number",
"value": 40.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Schedule Mod",
"variable_class": "basic",
"value_type": "number",
"value": 100.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Description",
"variable_class": "basic",
"value_type": "string",
"value": "BRAKE PROGRAMMING",
"row": null,
"options": null,
"type": "string"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "PG-B",
"operation_definition_name": "PG-B",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 3,
"runtime": 0.0,
"setup_time": 0.0
},
{
"id": 6170619,
"category": "operation",
"cost": "10.68",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "LZGP",
"row": {
"WORKGROUP": "LZGP",
"WORKCENTER": "LSR2",
"row_number": 8,
"Description": "AMADA FOMII 3015 RI",
"BILLING_RATE": 90.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 90.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Thickness",
"variable_class": "basic",
"value_type": "number",
"value": 0.048,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Use Manual Laser Length",
"variable_class": "drop_down",
"value_type": "string",
"value": "No",
"row": null,
"options": [
"No",
"Yes"
],
"type": "string"
},
{
"label": "Cut Length",
"variable_class": "basic",
"value_type": "number",
"value": 41.28814,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Pierce Count",
"variable_class": "basic",
"value_type": "number",
"value": 1.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Cut Rates",
"variable_class": "table",
"value_type": "number",
"value": 200.0,
"row": {
"cut_rate": 200.0,
"thickness": 0.0538,
"row_number": 57,
"pierce_time": 1.0,
"material_family": "Carbon Steel"
},
"options": null,
"type": "table"
},
{
"label": "Material Cut Rate",
"variable_class": "basic",
"value_type": "number",
"value": 200.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Mat Pierce Time",
"variable_class": "basic",
"value_type": "number",
"value": 1.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 268.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.0037313432835820895,
"row": null,
"options": null,
"type": "number"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.1,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "LZGP | 41.29 Cut Inches",
"operation_definition_name": "LZGP",
"notes": null,
"quantities": [
{
"price": "9.34",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "10.68",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "12.36",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "15.72",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 4,
"runtime": 0.0037313432835820895,
"setup_time": 0.1
},
{
"id": 6170620,
"category": "operation",
"cost": "13.27",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "FORM",
"row": {
"WORKGROUP": "FORM",
"WORKCENTER": "HDS",
"row_number": 5,
"Description": "HDS AMADA BRAKE PRES",
"BILLING_RATE": 49.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 49.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Bend Count",
"variable_class": "basic",
"value_type": "number",
"value": 1.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.25,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Run Time Per Bend (seconds)",
"variable_class": "basic",
"value_type": "number",
"value": 15.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 240.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.004166666666666667,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "FORM | 1.0 Bends",
"operation_definition_name": "FORM",
"notes": null,
"quantities": [
{
"price": "12.45",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "13.27",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "14.29",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "16.33",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 5,
"runtime": 0.004166666666666667,
"setup_time": 0.25
},
{
"id": 6170621,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "FW",
"operation_definition_name": "FW",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 6,
"runtime": null,
"setup_time": null
},
{
"id": 6170622,
"category": "operation",
"cost": "10.61",
"costing_variables": [
{
"label": "Labor Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "OSP Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 25.0,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Total Markup",
"operation_definition_name": "Total Markup",
"notes": null,
"quantities": [
{
"price": "12.55",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "10.61",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "14.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "20.78",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 7,
"runtime": null,
"setup_time": null
}
],
"supporting_files": [
{
"filename": "flat.step",
"url": "Test.url"
}
],
"thumbnail_url": "Test.url",
"type": "manufactured",
"deliver_quantity": 5,
"make_quantity": 5
},
{
"id": 1185150,
"child_ids": [],
"children": [],
"description": "HOUSING",
"export_controlled": false,
"finishes": [],
"innate_quantity": 1,
"is_root_component": false,
"material": {
"id": 56691,
"display_name": null,
"family": "Carbon Steel",
"material_class": "Metal",
"name": "Carbon Steel A36"
},
"material_operations": [
{
"id": 6170608,
"category": "material",
"cost": "299.06",
"costing_variables": [
{
"label": "Part Length (in)",
"variable_class": "basic",
"value_type": "number",
"value": 45.85558,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Width (in)",
"variable_class": "basic",
"value_type": "number",
"value": 31.62386,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Thickness (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.075,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Webbing (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.35,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Selection",
"variable_class": "table",
"value_type": "string",
"value": "MS14G60X120",
"row": {
"PART": "MS14G60X120",
"WIDTH": 60.0,
"LENGTH": 120.0,
"AMT_COST": 119.6244,
"THICKNESS": 0.075,
"row_number": 131,
"DESCRIPTION": "14 Ga. HRPO 60x120",
"PRODUCT_LINE": "RM",
"UM_INVENTORY": "EA"
},
"options": null,
"type": "table"
},
{
"label": "Material Description",
"variable_class": "basic",
"value_type": "string",
"value": "14 Ga. HRPO 60x120",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Sheet Length (in)",
"variable_class": "basic",
"value_type": "number",
"value": 120.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Width (in)",
"variable_class": "basic",
"value_type": "number",
"value": 60.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Thickness (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.075,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Sheet",
"variable_class": "basic",
"value_type": "number",
"value": 2.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Weight",
"variable_class": "basic",
"value_type": "number",
"value": 153.144,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Gross Weight",
"variable_class": "basic",
"value_type": "number",
"value": 76.572,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Net Weight",
"variable_class": "basic",
"value_type": "number",
"value": 14.591,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Cost Per Sheet",
"variable_class": "basic",
"value_type": "currency",
"value": 119.6244,
"row": null,
"options": null,
"type": "currency"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Material | 14 Ga. HRPO 60x120",
"operation_definition_name": "Sheet | Material",
"notes": null,
"quantities": [
{
"price": "59.81",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "299.06",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "598.12",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "1196.24",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 1,
"runtime": null,
"setup_time": null
}
],
"parent_ids": [
1185146
],
"part_custom_attrs": [],
"part_name": "57-007-00002-N-1.step",
"part_number": "57-007-00002-N-1",
"part_url": "Test.url",
"process": {
"id": 7559,
"external_name": "Sheet Metal Fabrication",
"name": "Laser & Form"
},
"purchased_component": null,
"revision": null,
"shop_operations": [
{
"id": 6170609,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "ENG",
"operation_definition_name": "ENG",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 2,
"runtime": null,
"setup_time": null
},
{
"id": 6170610,
"category": "operation",
"cost": "0",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "PG-B",
"row": {
"Department": "",
"Workcenter": "PG-B",
"row_number": 16,
"Description": "BRAKE PROGRAMMING",
"Billing_Rate": 32.0,
"Hours_per_Week": 40.0,
"Schedule_Percent_Modifier": 1.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 32.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Hours Per Week",
"variable_class": "basic",
"value_type": "number",
"value": 40.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Schedule Mod",
"variable_class": "basic",
"value_type": "number",
"value": 100.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Description",
"variable_class": "basic",
"value_type": "string",
"value": "BRAKE PROGRAMMING",
"row": null,
"options": null,
"type": "string"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "PG-B",
"operation_definition_name": "PG-B",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 3,
"runtime": 0.0,
"setup_time": 0.0
},
{
"id": 6170611,
"category": "operation",
"cost": "14.07",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "LZGP",
"row": {
"WORKGROUP": "LZGP",
"WORKCENTER": "LSR2",
"row_number": 8,
"Description": "AMADA FOMII 3015 RI",
"BILLING_RATE": 90.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 90.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Thickness",
"variable_class": "basic",
"value_type": "number",
"value": 0.075,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Use Manual Laser Length",
"variable_class": "drop_down",
"value_type": "string",
"value": "No",
"row": null,
"options": [
"No",
"Yes"
],
"type": "string"
},
{
"label": "Cut Length",
"variable_class": "basic",
"value_type": "number",
"value": 154.95888000000002,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Pierce Count",
"variable_class": "basic",
"value_type": "number",
"value": 16.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Cut Rates",
"variable_class": "table",
"value_type": "number",
"value": 155.0,
"row": {
"cut_rate": 155.0,
"thickness": 0.1046,
"row_number": 54,
"pierce_time": 1.0,
"material_family": "Carbon Steel"
},
"options": null,
"type": "table"
},
{
"label": "Material Cut Rate",
"variable_class": "basic",
"value_type": "number",
"value": 155.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Mat Pierce Time",
"variable_class": "basic",
"value_type": "number",
"value": 1.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 47.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.02127659574468085,
"row": null,
"options": null,
"type": "number"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.05,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "LZGP | 154.96 Cut Inches",
"operation_definition_name": "LZGP",
"notes": null,
"quantities": [
{
"price": "6.41",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "14.07",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "23.65",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "42.80",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 4,
"runtime": 0.02127659574468085,
"setup_time": 0.05
},
{
"id": 6170612,
"category": "operation",
"cost": "69.42",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "FORM",
"row": {
"WORKGROUP": "FORM",
"WORKCENTER": "HDS",
"row_number": 5,
"Description": "HDS AMADA BRAKE PRES",
"BILLING_RATE": 49.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 49.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Bend Count",
"variable_class": "basic",
"value_type": "number",
"value": 3.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.25,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Run Time Per Bend (seconds)",
"variable_class": "basic",
"value_type": "number",
"value": 15.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 80.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.23333333333333334,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "FORM | 3.0 Bends",
"operation_definition_name": "FORM",
"notes": "INSTALL PRESSNUTS",
"quantities": [
{
"price": "23.68",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "69.42",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "126.58",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "240.92",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 5,
"runtime": 0.23333333333333334,
"setup_time": 0.25
},
{
"id": 6170613,
"category": "operation",
"cost": "15.31",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "FORM",
"row": {
"WORKGROUP": "FORM",
"WORKCENTER": "HDS",
"row_number": 5,
"Description": "HDS AMADA BRAKE PRES",
"BILLING_RATE": 49.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 49.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Bend Count",
"variable_class": "basic",
"value_type": "number",
"value": 3.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.25,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Run Time Per Bend (seconds)",
"variable_class": "basic",
"value_type": "number",
"value": 15.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 80.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.0125,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "FORM | 3.0 Bends",
"operation_definition_name": "FORM",
"notes": null,
"quantities": [
{
"price": "12.86",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "15.31",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "18.38",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "24.50",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 6,
"runtime": 0.0125,
"setup_time": 0.25
},
{
"id": 6170614,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "FW",
"operation_definition_name": "FW",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 7,
"runtime": null,
"setup_time": null
},
{
"id": 6170615,
"category": "operation",
"cost": "135.27",
"costing_variables": [
{
"label": "Labor Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "OSP Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 25.0,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Total Markup",
"operation_definition_name": "Total Markup",
"notes": null,
"quantities": [
{
"price": "55.50",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "135.27",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "260.69",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "511.52",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 8,
"runtime": null,
"setup_time": null
}
],
"supporting_files": [
{
"filename": "flat.step",
"url": "Test.url"
}
],
"thumbnail_url": "Test.url",
"type": "manufactured",
"deliver_quantity": 5,
"make_quantity": 5
},
{
"id": 1185149,
"child_ids": [],
"children": [],
"description": "FORMED PLATE",
"export_controlled": false,
"finishes": [],
"innate_quantity": 1,
"is_root_component": false,
"material": {
"id": 56691,
"display_name": null,
"family": "Carbon Steel",
"material_class": "Metal",
"name": "Carbon Steel A36"
},
"material_operations": [
{
"id": 6170601,
"category": "material",
"cost": "37.38",
"costing_variables": [
{
"label": "Part Length (in)",
"variable_class": "basic",
"value_type": "number",
"value": 28.92735,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Width (in)",
"variable_class": "basic",
"value_type": "number",
"value": 15.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Thickness (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.075,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Webbing (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.35,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Selection",
"variable_class": "table",
"value_type": "string",
"value": "MS14G60X120",
"row": {
"PART": "MS14G60X120",
"WIDTH": 60.0,
"LENGTH": 120.0,
"AMT_COST": 119.6244,
"THICKNESS": 0.075,
"row_number": 131,
"DESCRIPTION": "14 Ga. HRPO 60x120",
"PRODUCT_LINE": "RM",
"UM_INVENTORY": "EA"
},
"options": null,
"type": "table"
},
{
"label": "Material Description",
"variable_class": "basic",
"value_type": "string",
"value": "14 Ga. HRPO 60x120",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Sheet Length (in)",
"variable_class": "basic",
"value_type": "number",
"value": 120.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Width (in)",
"variable_class": "basic",
"value_type": "number",
"value": 60.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Thickness (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.075,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Sheet",
"variable_class": "basic",
"value_type": "number",
"value": 16.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Weight",
"variable_class": "basic",
"value_type": "number",
"value": 153.144,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Gross Weight",
"variable_class": "basic",
"value_type": "number",
"value": 9.572,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Net Weight",
"variable_class": "basic",
"value_type": "number",
"value": 8.441,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Cost Per Sheet",
"variable_class": "basic",
"value_type": "currency",
"value": 119.6244,
"row": null,
"options": null,
"type": "currency"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Material | 14 Ga. HRPO 60x120",
"operation_definition_name": "Sheet | Material",
"notes": null,
"quantities": [
{
"price": "7.48",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "37.38",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "74.77",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "149.53",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 1,
"runtime": null,
"setup_time": null
}
],
"parent_ids": [
1185146
],
"part_custom_attrs": [],
"part_name": "57-007-00002-N-2.step",
"part_number": "57-007-00002-N-2",
"part_url": "Test.url",
"process": {
"id": 7559,
"external_name": "Sheet Metal Fabrication",
"name": "Laser & Form"
},
"purchased_component": null,
"revision": null,
"shop_operations": [
{
"id": 6170602,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "ENG",
"operation_definition_name": "ENG",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 2,
"runtime": null,
"setup_time": null
},
{
"id": 6170603,
"category": "operation",
"cost": "0",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "PG-B",
"row": {
"Department": "",
"Workcenter": "PG-B",
"row_number": 16,
"Description": "BRAKE PROGRAMMING",
"Billing_Rate": 32.0,
"Hours_per_Week": 40.0,
"Schedule_Percent_Modifier": 1.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 32.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Hours Per Week",
"variable_class": "basic",
"value_type": "number",
"value": 40.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Schedule Mod",
"variable_class": "basic",
"value_type": "number",
"value": 100.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Description",
"variable_class": "basic",
"value_type": "string",
"value": "BRAKE PROGRAMMING",
"row": null,
"options": null,
"type": "string"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "PG-B",
"operation_definition_name": "PG-B",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 3,
"runtime": 0.0,
"setup_time": 0.0
},
{
"id": 6170604,
"category": "operation",
"cost": "10.20",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "LZGP",
"row": {
"WORKGROUP": "LZGP",
"WORKCENTER": "LSR2",
"row_number": 8,
"Description": "AMADA FOMII 3015 RI",
"BILLING_RATE": 90.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 90.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Thickness",
"variable_class": "basic",
"value_type": "number",
"value": 0.075,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Use Manual Laser Length",
"variable_class": "drop_down",
"value_type": "string",
"value": "No",
"row": null,
"options": [
"No",
"Yes"
],
"type": "string"
},
{
"label": "Cut Length",
"variable_class": "basic",
"value_type": "number",
"value": 87.85470000000001,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Pierce Count",
"variable_class": "basic",
"value_type": "number",
"value": 11.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Cut Rates",
"variable_class": "table",
"value_type": "number",
"value": 155.0,
"row": {
"cut_rate": 155.0,
"thickness": 0.1046,
"row_number": 54,
"pierce_time": 1.0,
"material_family": "Carbon Steel"
},
"options": null,
"type": "table"
},
{
"label": "Material Cut Rate",
"variable_class": "basic",
"value_type": "number",
"value": 155.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Mat Pierce Time",
"variable_class": "basic",
"value_type": "number",
"value": 1.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 79.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.012658227848101266,
"row": null,
"options": null,
"type": "number"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.05,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "LZGP | 87.85 Cut Inches",
"operation_definition_name": "LZGP",
"notes": null,
"quantities": [
{
"price": "5.64",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "10.20",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "15.89",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "27.28",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 4,
"runtime": 0.012658227848101266,
"setup_time": 0.05
},
{
"id": 6170605,
"category": "operation",
"cost": "14.29",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "FORM",
"row": {
"WORKGROUP": "FORM",
"WORKCENTER": "HDS",
"row_number": 5,
"Description": "HDS AMADA BRAKE PRES",
"BILLING_RATE": 49.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 49.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Bend Count",
"variable_class": "basic",
"value_type": "number",
"value": 2.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.25,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Run Time Per Bend (seconds)",
"variable_class": "basic",
"value_type": "number",
"value": 15.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 120.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.008333333333333333,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "FORM | 2.0 Bends",
"operation_definition_name": "FORM",
"notes": null,
"quantities": [
{
"price": "12.66",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "14.29",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "16.33",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "20.42",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 5,
"runtime": 0.008333333333333333,
"setup_time": 0.25
},
{
"id": 6170606,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "FW",
"operation_definition_name": "FW",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 6,
"runtime": null,
"setup_time": null
},
{
"id": 6170607,
"category": "operation",
"cost": "21.04",
"costing_variables": [
{
"label": "Labor Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "OSP Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 25.0,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Total Markup",
"operation_definition_name": "Total Markup",
"notes": null,
"quantities": [
{
"price": "13.92",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "21.04",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "36.38",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "67.06",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 7,
"runtime": null,
"setup_time": null
}
],
"supporting_files": [
{
"filename": "flat.step",
"url": "Test.url"
}
],
"thumbnail_url": "Test.url",
"type": "manufactured",
"deliver_quantity": 5,
"make_quantity": 5
},
{
"id": 1185148,
"child_ids": [],
"children": [],
"description": "1/4-20 PRESS FIT NUT SS PEM",
"export_controlled": false,
"finishes": [],
"innate_quantity": 14,
"is_root_component": false,
"material": null,
"material_operations": [
{
"id": 6170599,
"category": "material",
"cost": "185.50",
"costing_variables": [
{
"label": "piece_price",
"variable_class": "basic",
"value_type": "currency",
"value": 2.65,
"row": null,
"options": null,
"type": "currency"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "PC Piece Price",
"operation_definition_name": "PC Piece Price",
"notes": null,
"quantities": [
{
"price": "37.10",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "185.50",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "371.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "742.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 1,
"runtime": null,
"setup_time": null
},
{
"id": 6170600,
"category": "material",
"cost": "63.07",
"costing_variables": [
{
"label": "Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Material Markup 34.0%",
"operation_definition_name": "Material Markup",
"notes": null,
"quantities": [
{
"price": "12.61",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "63.07",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "126.14",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "252.28",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 2,
"runtime": null,
"setup_time": null
}
],
"parent_ids": [
1185146
],
"part_custom_attrs": [],
"part_name": "11-001-00003-N_NutPress_4-20_SS_XX.step",
"part_number": "LAC-0420-2MD",
"part_url": "Test.url",
"process": {
"id": 4922,
"external_name": null,
"name": "Purchased Components"
},
"purchased_component": {
"oem_part_number": "LAC-0420-2MD",
"internal_part_number": "LAC-0420-2MD",
"description": "1/4-20 PRESS FIT NUT SS PEM",
"piece_price": "2.6500",
"properties": [
{
"name": "Alt_cost",
"code_name": "alt_cost",
"value_type": "numeric",
"value": null
}
]
},
"revision": null,
"shop_operations": [],
"supporting_files": [],
"thumbnail_url": "Test.url",
"type": "purchased",
"deliver_quantity": 70,
"make_quantity": 70
},
{
"id": 1185147,
"child_ids": [],
"children": [],
"description": "FORMED SECTION",
"export_controlled": false,
"finishes": [],
"innate_quantity": 1,
"is_root_component": false,
"material": {
"id": 56691,
"display_name": null,
"family": "Carbon Steel",
"material_class": "Metal",
"name": "Carbon Steel A36"
},
"material_operations": [
{
"id": 6170592,
"category": "material",
"cost": "11.45",
"costing_variables": [
{
"label": "Part Length (in)",
"variable_class": "basic",
"value_type": "number",
"value": 27.52341,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Width (in)",
"variable_class": "basic",
"value_type": "number",
"value": 5.97338,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Thickness (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.048,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Webbing (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.35,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Selection",
"variable_class": "table",
"value_type": "string",
"value": "MS18G60X120",
"row": {
"PART": "MS18G60X120",
"WIDTH": 60.0,
"LENGTH": 120.0,
"AMT_COST": 91.5884,
"THICKNESS": 0.05,
"row_number": 140,
"DESCRIPTION": "18 Ga. CRS 60x120",
"PRODUCT_LINE": "RM",
"UM_INVENTORY": "EA"
},
"options": null,
"type": "table"
},
{
"label": "Material Description",
"variable_class": "basic",
"value_type": "string",
"value": "18 Ga. CRS 60x120",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Sheet Length (in)",
"variable_class": "basic",
"value_type": "number",
"value": 120.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Width (in)",
"variable_class": "basic",
"value_type": "number",
"value": 60.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Thickness (in)",
"variable_class": "basic",
"value_type": "number",
"value": 0.05,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Sheet",
"variable_class": "basic",
"value_type": "number",
"value": 40.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sheet Weight",
"variable_class": "basic",
"value_type": "number",
"value": 102.096,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Gross Weight",
"variable_class": "basic",
"value_type": "number",
"value": 2.552,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Net Weight",
"variable_class": "basic",
"value_type": "number",
"value": 1.32,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Cost Per Sheet",
"variable_class": "basic",
"value_type": "currency",
"value": 91.5884,
"row": null,
"options": null,
"type": "currency"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Material | 18 Ga. CRS 60x120",
"operation_definition_name": "Sheet | Material",
"notes": null,
"quantities": [
{
"price": "2.29",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "11.45",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "22.90",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "45.79",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 1,
"runtime": null,
"setup_time": null
}
],
"parent_ids": [
1185146
],
"part_custom_attrs": [],
"part_name": "57-007-00002-N-5.step",
"part_number": "57-007-00002-N-5",
"part_url": "Test.url",
"process": {
"id": 7559,
"external_name": "Sheet Metal Fabrication",
"name": "Laser & Form"
},
"purchased_component": null,
"revision": null,
"shop_operations": [
{
"id": 6170593,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "ENG",
"operation_definition_name": "ENG",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 2,
"runtime": null,
"setup_time": null
},
{
"id": 6170594,
"category": "operation",
"cost": "0",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "PG-B",
"row": {
"Department": "",
"Workcenter": "PG-B",
"row_number": 16,
"Description": "BRAKE PROGRAMMING",
"Billing_Rate": 32.0,
"Hours_per_Week": 40.0,
"Schedule_Percent_Modifier": 1.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 32.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Hours Per Week",
"variable_class": "basic",
"value_type": "number",
"value": 40.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Schedule Mod",
"variable_class": "basic",
"value_type": "number",
"value": 100.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Description",
"variable_class": "basic",
"value_type": "string",
"value": "BRAKE PROGRAMMING",
"row": null,
"options": null,
"type": "string"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "PG-B",
"operation_definition_name": "PG-B",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 3,
"runtime": 0.0,
"setup_time": 0.0
},
{
"id": 6170595,
"category": "operation",
"cost": "11.65",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "LZGP",
"row": {
"WORKGROUP": "LZGP",
"WORKCENTER": "LSR2",
"row_number": 8,
"Description": "AMADA FOMII 3015 RI",
"BILLING_RATE": 90.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 90.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Thickness",
"variable_class": "basic",
"value_type": "number",
"value": 0.048,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Use Manual Laser Length",
"variable_class": "drop_down",
"value_type": "string",
"value": "No",
"row": null,
"options": [
"No",
"Yes"
],
"type": "string"
},
{
"label": "Cut Length",
"variable_class": "basic",
"value_type": "number",
"value": 66.99358,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Pierce Count",
"variable_class": "basic",
"value_type": "number",
"value": 1.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Cut Rates",
"variable_class": "table",
"value_type": "number",
"value": 200.0,
"row": {
"cut_rate": 200.0,
"thickness": 0.0538,
"row_number": 57,
"pierce_time": 1.0,
"material_family": "Carbon Steel"
},
"options": null,
"type": "table"
},
{
"label": "Material Cut Rate",
"variable_class": "basic",
"value_type": "number",
"value": 200.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Mat Pierce Time",
"variable_class": "basic",
"value_type": "number",
"value": 1.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 170.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.0058823529411764705,
"row": null,
"options": null,
"type": "number"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.1,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "LZGP | 66.99 Cut Inches",
"operation_definition_name": "LZGP",
"notes": null,
"quantities": [
{
"price": "9.53",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "11.65",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "14.29",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "19.59",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 4,
"runtime": 0.0058823529411764705,
"setup_time": 0.1
},
{
"id": 6170596,
"category": "operation",
"cost": "14.29",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "FORM",
"row": {
"WORKGROUP": "FORM",
"WORKCENTER": "HDS",
"row_number": 5,
"Description": "HDS AMADA BRAKE PRES",
"BILLING_RATE": 49.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 49.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Bend Count",
"variable_class": "basic",
"value_type": "number",
"value": 2.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.25,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Run Time Per Bend (seconds)",
"variable_class": "basic",
"value_type": "number",
"value": 15.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 120.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.008333333333333333,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "FORM | 2.0 Bends",
"operation_definition_name": "FORM",
"notes": null,
"quantities": [
{
"price": "12.66",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "14.29",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "16.33",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "20.42",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 5,
"runtime": 0.008333333333333333,
"setup_time": 0.25
},
{
"id": 6170597,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "FW",
"operation_definition_name": "FW",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 6,
"runtime": null,
"setup_time": null
},
{
"id": 6170598,
"category": "operation",
"cost": "12.71",
"costing_variables": [
{
"label": "Labor Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "OSP Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 25.0,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Total Markup",
"operation_definition_name": "Total Markup",
"notes": null,
"quantities": [
{
"price": "13.22",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "12.71",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "18.20",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "29.17",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 7,
"runtime": null,
"setup_time": null
}
],
"supporting_files": [
{
"filename": "flat.step",
"url": "Test.url"
}
],
"thumbnail_url": "Test.url",
"type": "manufactured",
"deliver_quantity": 5,
"make_quantity": 5
},
{
"id": 1185146,
"child_ids": [
1185149,
1185150,
1185154,
1185152,
1185148,
1185147,
1185151,
1185153
],
"children": [
{
"child_id": 1185149,
"quantity": 1
},
{
"child_id": 1185150,
"quantity": 1
},
{
"child_id": 1185154,
"quantity": 1
},
{
"child_id": 1185152,
"quantity": 1
},
{
"child_id": 1185148,
"quantity": 14
},
{
"child_id": 1185147,
"quantity": 1
},
{
"child_id": 1185151,
"quantity": 1
},
{
"child_id": 1185153,
"quantity": 1
}
],
"description": "MOUNT AC",
"export_controlled": false,
"finishes": [],
"innate_quantity": 1,
"is_root_component": true,
"material": {
"id": 56691,
"display_name": null,
"family": "Carbon Steel",
"material_class": "Metal",
"name": "Carbon Steel A36"
},
"material_operations": [],
"parent_ids": [],
"part_custom_attrs": [],
"part_name": "57-007-00002-N_Mount_AC_RevP.stp",
"part_number": "57-007-00002-N2",
"part_url": "Test.url",
"part_uuid": "2529af5e-70ba-4722-bd11-b24f5fb51113",
"process": {
"id": 7561,
"external_name": "Sheet Metal",
"name": "Assembly with Welding"
},
"purchased_component": null,
"revision": "RP2",
"shop_operations": [
{
"id": 6170585,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "ENG",
"operation_definition_name": "ENG",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 1,
"runtime": null,
"setup_time": null
},
{
"id": 6170586,
"category": "operation",
"cost": "410.00",
"costing_variables": [
{
"label": "Weld Group",
"variable_class": "basic",
"value_type": "string",
"value": "WSTL",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "WSTL",
"row": {
"WORKGROUP": "WSTL",
"WORKCENTER": "WD01",
"row_number": 18,
"Description": "STL/SS WELD",
"BILLING_RATE": 40.0
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 40.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Segments",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Total Length",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Setup Time Per Segment",
"variable_class": "basic",
"value_type": "number",
"value": 5.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.25,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Weld Speed",
"variable_class": "basic",
"value_type": "number",
"value": 1.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 2.0,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "WSTL",
"operation_definition_name": "WELD",
"notes": null,
"quantities": [
{
"price": "90.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "410.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "810.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "1610.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 2,
"runtime": 2.0,
"setup_time": 0.25
},
{
"id": 6170587,
"category": "operation",
"cost": "65.37",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "GRD",
"row": {
"Department": "GRND",
"Workcenter": "GRD",
"row_number": 7,
"Description": "Hand Held Grinder",
"Billing_Rate": 37.0,
"Hours_per_Week": 50.0,
"Schedule_Percent_Modifier": 0.9
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 37.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Hours Per Week",
"variable_class": "basic",
"value_type": "number",
"value": 50.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Schedule Mod",
"variable_class": "basic",
"value_type": "number",
"value": 90.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Description",
"variable_class": "basic",
"value_type": "string",
"value": "Hand Held Grinder",
"row": null,
"options": null,
"type": "string"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.1,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.3333333333333333,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "GRD",
"operation_definition_name": "GRD",
"notes": null,
"quantities": [
{
"price": "16.03",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "65.37",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "127.03",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "250.37",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 3,
"runtime": 0.3333333333333333,
"setup_time": 0.1
},
{
"id": 6170588,
"category": "operation",
"cost": "28.37",
"costing_variables": [
{
"label": "Workcenter Lookup",
"variable_class": "table",
"value_type": "string",
"value": "QCI",
"row": {
"Department": "SHOP",
"Workcenter": "QCI",
"row_number": 51,
"Description": "Quality Control - In",
"Billing_Rate": 37.0,
"Hours_per_Week": 80.0,
"Schedule_Percent_Modifier": 2.4
},
"options": null,
"type": "table"
},
{
"label": "Bill Rate",
"variable_class": "basic",
"value_type": "currency",
"value": 37.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "setup_time",
"variable_class": "basic",
"value_type": "number",
"value": 0.1,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "runtime",
"variable_class": "basic",
"value_type": "number",
"value": 0.13333333333333333,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "QCI",
"operation_definition_name": "QCI",
"notes": null,
"quantities": [
{
"price": "8.63",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "28.37",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "53.03",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "102.37",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 4,
"runtime": 0.13333333333333333,
"setup_time": 0.1
},
{
"id": 6170589,
"category": "operation",
"cost": "0",
"costing_variables": [],
"is_finish": false,
"is_outside_service": false,
"name": "FS",
"operation_definition_name": "FS",
"notes": null,
"quantities": [
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "0.00",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 5,
"runtime": null,
"setup_time": null
},
{
"id": 6170590,
"category": "operation",
"cost": "410.33",
"costing_variables": [
{
"label": "Machine",
"variable_class": "basic",
"value_type": "string",
"value": "LPF-LAN",
"row": null,
"options": null,
"type": "string"
},
{
"label": "operation",
"variable_class": "table",
"value_type": "string",
"value": "LPF001",
"row": {
"machine": "LPF-LAN",
"operation": "LPF001",
"row_number": 13,
"description": "COLOR:"
},
"options": null,
"type": "table"
},
{
"label": "Product Code",
"variable_class": "basic",
"value_type": "string",
"value": "F2",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Router Template",
"variable_class": "drop_down",
"value_type": "string",
"value": "!LCF-B-P-KB",
"row": null,
"options": [
"No Template Selected",
"!LCF-B-KB",
"!LCF-B-KB-CK",
"!LCF-B-KB-STP",
"!LCF-B-P-KB",
"!LCF-BO-B-KB",
"!LCF-BO-B-P-KB",
"!LCF-M-B-M-KB",
"!LCF-M-B-M-KB-STP",
"!LCF-M-KB-STP"
],
"type": "string"
},
{
"label": "Powder Search",
"variable_class": "basic",
"value_type": "string",
"value": "Type to Search",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Powder Name",
"variable_class": "table",
"value_type": "string",
"value": "FREIGHTLINER WHITE",
"row": {
"Cost": 6.97,
"SORT_CODE": "FRTWHT",
"row_number": 19,
"PART_NUMBER": "PWS8-90164",
"POWDER_NAME": "FREIGHTLINER WHITE"
},
"options": null,
"type": "table"
},
{
"label": "Primer?",
"variable_class": "drop_down",
"value_type": "string",
"value": "No",
"row": null,
"options": [
"No",
"Yes"
],
"type": "string"
},
{
"label": "Primer Search",
"variable_class": "basic",
"value_type": "string",
"value": "UBS2-80001",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Primer Name",
"variable_class": "table",
"value_type": "string",
"value": "UBS2-80001",
"row": {
"cost": 6.42,
"sort_code": "ZRBLKU",
"row_number": 5,
"part_number": "EAS6-C0025",
"primer_name": "UBS2-80001"
},
"options": null,
"type": "table"
},
{
"label": "Primer, Sort Code",
"variable_class": "basic",
"value_type": "string",
"value": "ZRBLKU",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Primer, Part Number",
"variable_class": "basic",
"value_type": "string",
"value": "EAS6-C0025",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Primer, Cost",
"variable_class": "basic",
"value_type": "currency",
"value": 6.42,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Primer Specific Gravity",
"variable_class": "basic",
"value_type": "number",
"value": 2.83,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Primer Required Thickness",
"variable_class": "basic",
"value_type": "number",
"value": 1.5,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Primer Transfer Efficiency",
"variable_class": "basic",
"value_type": "number",
"value": 0.4,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Primer Part Cost per Sq Ft",
"variable_class": "basic",
"value_type": "currency",
"value": 0.35,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Primer Sqft per Pound",
"variable_class": "basic",
"value_type": "number",
"value": 18.12,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Lbs Primer per Part",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Sort Code",
"variable_class": "basic",
"value_type": "string",
"value": "FRTWHT",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Part Number",
"variable_class": "basic",
"value_type": "string",
"value": "PWS8-90164",
"row": null,
"options": null,
"type": "string"
},
{
"label": "Cost",
"variable_class": "basic",
"value_type": "currency",
"value": 6.97,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Powder Specific Gravity",
"variable_class": "basic",
"value_type": "number",
"value": 1.75,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Powder Required Thickness",
"variable_class": "basic",
"value_type": "number",
"value": 3.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Powder Transfer Efficiency",
"variable_class": "basic",
"value_type": "number",
"value": 0.4,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Cost per Sq Ft",
"variable_class": "basic",
"value_type": "currency",
"value": 0.48,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Powder Sqft per Pound",
"variable_class": "basic",
"value_type": "number",
"value": 14.65,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Lbs Powder per Part",
"variable_class": "basic",
"value_type": "number",
"value": 1.74,
"row": null,
"options": null,
"type": "number"
},
{
"label": "# Plugs & Caps",
"variable_class": "basic",
"value_type": "number",
"value": 14.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Plugs & Caps Cost",
"variable_class": "basic",
"value_type": "currency",
"value": 0.16,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Plugs & Caps Cost Each",
"variable_class": "basic",
"value_type": "currency",
"value": 2.24,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Tape Time, Mins",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Tape Time Cost, Min",
"variable_class": "basic",
"value_type": "currency",
"value": 1.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Tape Time Cost Each",
"variable_class": "basic",
"value_type": "currency",
"value": 0.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Caulking, Lineal In.",
"variable_class": "basic",
"value_type": "number",
"value": 50.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Caulking Cost, Per In.",
"variable_class": "basic",
"value_type": "currency",
"value": 0.16,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Caulking Cost Each",
"variable_class": "basic",
"value_type": "currency",
"value": 8.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Special Packaging, Qty / Ea",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Special Packaging, $ / Ea",
"variable_class": "basic",
"value_type": "currency",
"value": 0.16,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Special Packaging Cost",
"variable_class": "basic",
"value_type": "currency",
"value": 0.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Other, Qty / Ea",
"variable_class": "basic",
"value_type": "number",
"value": 0.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Other, $ / Ea",
"variable_class": "basic",
"value_type": "currency",
"value": 0.16,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Other Cost",
"variable_class": "basic",
"value_type": "currency",
"value": 0.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Part Area, sq/in",
"variable_class": "basic",
"value_type": "number",
"value": 3673.281,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Area, sq/ft",
"variable_class": "basic",
"value_type": "number",
"value": 25.509,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Hooks Per Part, Large",
"variable_class": "basic",
"value_type": "number",
"value": 8.93,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Per Hook, Small",
"variable_class": "basic",
"value_type": "number",
"value": 0.11,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Line Cost, hr",
"variable_class": "basic",
"value_type": "currency",
"value": 650.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Setup Cost",
"variable_class": "drop_down",
"value_type": "currency",
"value": 5,
"row": null,
"options": [
5,
10,
25,
50
],
"type": "currency"
},
{
"label": "Line Speed",
"variable_class": "drop_down",
"value_type": "number",
"value": 6,
"row": null,
"options": [
6,
5,
4,
3,
2,
1
],
"type": "number"
},
{
"label": "Density 1, parts",
"variable_class": "basic",
"value_type": "number",
"value": 1.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Density 2, per hook",
"variable_class": "basic",
"value_type": "number",
"value": 9.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Part Per Foot",
"variable_class": "basic",
"value_type": "number",
"value": 0.11,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Feet Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 300.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Pc Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 33.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "WC Cost",
"variable_class": "basic",
"value_type": "currency",
"value": 19.7,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Blasting Required?",
"variable_class": "drop_down",
"value_type": "string",
"value": "Yes",
"row": null,
"options": [
"None Selected",
"No",
"Yes"
],
"type": "string"
},
{
"label": "Blasting Cost, hr",
"variable_class": "basic",
"value_type": "currency",
"value": 53.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Blasting Parts Per Hour",
"variable_class": "basic",
"value_type": "number",
"value": 5.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Blasting Cost",
"variable_class": "basic",
"value_type": "currency",
"value": 10.6,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Top Coat Cost Final",
"variable_class": "basic",
"value_type": "currency",
"value": 12.24,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Primer Coat Cost Final",
"variable_class": "basic",
"value_type": "currency",
"value": 8.93,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Setup Cost Final",
"variable_class": "basic",
"value_type": "currency",
"value": 1.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Masking Cost Final",
"variable_class": "basic",
"value_type": "currency",
"value": 2.24,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Other Cost Final",
"variable_class": "basic",
"value_type": "currency",
"value": 0.0,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Blasting Cost Final",
"variable_class": "basic",
"value_type": "currency",
"value": 10.6,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Single Line Cost Final",
"variable_class": "basic",
"value_type": "currency",
"value": 19.7,
"row": null,
"options": null,
"type": "currency"
},
{
"label": "Markup %",
"variable_class": "basic",
"value_type": "number",
"value": 150.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Total Price Ea",
"variable_class": "basic",
"value_type": "currency",
"value": 410.33,
"row": null,
"options": null,
"type": "currency"
}
],
"is_finish": false,
"is_outside_service": true,
"name": "LPF-LAN",
"operation_definition_name": "LPF-LAN",
"notes": null,
"quantities": [
{
"price": "88.06",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "410.33",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "813.15",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "1618.80",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 6,
"runtime": null,
"setup_time": null
},
{
"id": 6170591,
"category": "operation",
"cost": "273.85",
"costing_variables": [
{
"label": "Labor Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "Material Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 34.0,
"row": null,
"options": null,
"type": "number"
},
{
"label": "OSP Markup (%)",
"variable_class": "basic",
"value_type": "number",
"value": 25.0,
"row": null,
"options": null,
"type": "number"
}
],
"is_finish": false,
"is_outside_service": false,
"name": "Total Markup",
"operation_definition_name": "Total Markup",
"notes": null,
"quantities": [
{
"price": "83.94",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 1
},
{
"price": "273.85",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 5
},
{
"price": "539.91",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 10
},
{
"price": "1072.03",
"manual_price": null,
"lead_time": 0,
"manual_lead_time": null,
"quantity": 20
}
],
"position": 7,
"runtime": null,
"setup_time": null
}
],
"supporting_files": [
{
"filename": "57-007-00002-N_Mount_AC_RevP.pdf",
"url": "Test.url"
}
],
"thumbnail_url": "Test.url",
"type": "assembled",
"deliver_quantity": 5,
"make_quantity": 5
}
],
"description": "MOUNT AC",
"expedite_revenue": null,
"export_controlled": false,
"filename": "57-007-00002-N_Mount_AC_RevP.stp",
"lead_days": 1,
"markup_1_price": "0.00",
"markup_1_name": "Overhead",
"markup_2_price": "0.00",
"markup_2_name": "Markup",
"private_notes": null,
"public_notes": "",
"quantity": 5,
"quantity_outstanding": 5,
"quote_item_id": 778769,
"quote_item_type": "automatic",
"root_component_id": 1185146,
"ships_on": "2021-10-13",
"total_price": "2459.10",
"unit_price": "491.82",
"base_price": "2459.10",
"add_on_fees": null,
"ordered_add_ons": [],
"pricing_items": []
}
],
"payment_details": {
"card_brand": null,
"card_last4": null,
"net_payout": "2459.10",
"payment_type": null,
"purchase_order_number": null,
"purchasing_dept_contact_email": null,
"purchasing_dept_contact_name": null,
"shipping_cost": "0.00",
"subtotal": "2459.10",
"tax_cost": "0.00",
"tax_rate": "0.000",
"payment_terms": null,
"total_price": "2459.10"
},
"private_notes": "",
"quote_erp_code": null,
"quote_number": 18,
"quote_revision_number": null,
"sales_person": {
"first_name": "Jon",
"last_name": "Grose",
"email": "jonathan.grose+zpi@paperlessparts.com"
},
"salesperson": {
"first_name": "Jon",
"last_name": "Grose",
"email": "jonathan.grose+zpi@paperlessparts.com"
},
"shipments": [],
"shipping_info": {
"id": 83912,
"attention": "Jon Grose",
"address1": "456 MakeBelieve Ave",
"address2": "",
"business_name": "Waffle Dreams",
"city": "Springville",
"country": "USA",
"facility_name": "",
"phone": null,
"phone_ext": null,
"postal_code": "52336",
"state": "IA"
},
"shipping_option": null,
"ships_on": "2021-10-13",
"status": "pending",
"send_from_facility": {
"name": "G.S. Precision, Inc.",
"address": {
"address1": "101 John Seitz Drive",
"address2": "",
"city": "Brattleboro",
"country": "USA",
"postal_code": "05301-3642",
"state": "VT",
"erp_code": null
},
"is_default": true,
"phone": "8022575200",
"phone_ext": "",
"url": "www.gsprecision.com"
}
}
"""

    return json.loads(json_str)
