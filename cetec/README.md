Paperless Parts / Cetec Order Export Integration
------------------------------------------------

Cetec is a cloud-based ERP system with limited API functionality. The order export from Paperless Parts to Cetec involves two primary API calls.
* **Part Revision Definition** For each order item, we supply a nested tree structure of information describing the part or assembly to an endpoint called /partrevisiondefinition. Each node in the JSON tree we construct corresponds to a component in Paperless Parts. Each node in the tree can have a `bom_definition`, which is an array of JSON objects representing the subcomponents that comprise the current component, as well as an array of `locations` which represent the operations required to produce the current component. Note that each subsequent call to this endpoint for a given top-level part number will blow away and then replace the BOM definition for that part number. Consider the following example JSON payload that describes a simple assembly with a top-level assembled component, as well as a child manufactured component (with raw material) and a child purchased component:

```
{
  "prcpart": "PRT TESTASSEMBLY",
  "revision_text": "E",
  "bom_definition": [
    {
      "prcpart": "SUB TESTMANUFACTURED",
      "revision_text": "H",
      "qty_per_top": 1,
      "bom_definition": [
        {
          "component": 1,
          "prcpart": "RAW MATERIAL",
          "sourcing": "",
          "pick_comments": "",
          "qty_per_top": 1
        }
      ],
      "locations": [
        {
          "location_external_key": "admin",
          "build_order": 1,
          "operations": [
            {
              "operation_external_key": "generic_1_sec_operation",
              "repetitions": 540,
              "setup": true,
              "place_in_line": 1,
              "instructions": []
            }
          ]
        },
        {
          "location_external_key": "cnc_milling",
          "build_order": 2,
          "operations": [
            {
              "operation_external_key": "generic_1_sec_operation",
              "repetitions": 7200,
              "setup": true,
              "place_in_line": 2,
              "instructions": []
            }
          ]
        }
      ]
    },
    {
      "prcpart": "COM PURCHASEDCOMPONENT",
      "revision_text": "",
      "qty_per_top": 3
    }
  ],
  "locations": [
    {
      "location_external_key": "admin",
      "build_order": 1,
      "operations": [
        {
          "operation_external_key": "generic_1_sec_operation",
          "repetitions": 540,
          "setup": true,
          "place_in_line": 1,
          "instructions": []
        }
      ]
    },
    {
      "location_external_key": "assembly",
      "build_order": 2,
      "operations": [
        {
          "operation_external_key": "generic_1_sec_operation",
          "repetitions": 1,
          "setup": false,
          "place_in_line": 2,
          "instructions": []
        }
      ]
    }
  ],
  "preshared_token": "<token>"
}
```
* **Import JSON** Once the BOM definitions have been created for each order item using the above partrevisiondefinition endpoint, the importjson endpoint is used to create the sales order and workorders for the various components that need to be produced. Here is an example of the JSON payload for this endpoint:

```
[
  {
    "location": "MN",
    "shipto_name": "Bob Loblaw",
    "shipto_address_1": "205 PORTLAND ST",
    "shipto_address_2": "",
    "shipto_address_3": "",
    "shipto_address_4": "",
    "shipto_city": "BOSTON",
    "shipto_state": "MA",
    "shipto_zip": "02114",
    "billto_name": "Bob Loblaw",
    "billto_address_1": "205 PORTLAND ST",
    "billto_address_2": "",
    "billto_address_3": "",
    "billto_address_4": "",
    "billto_city": "BOSTON",
    "billto_state": "MA",
    "billto_zip": "02114",
    "external_key": "366365",
    "internal_comments": "Order Number: <a href=\"https://app.paperlessparts.com/orders/edit/366\">366</a><br><br>",
    "commission_note": "Salesperson: Sales Person (sales.person@paperlessparts.com)",
    "ship_via": "pickup",
    "shipping_instructions": "",
    "customer_taxtype": "1",
    "tax_collected": "0.00",
    "place_order": true,
    "internal_customer_id": "1",
    "internal_vendor_id": "1",
    "customer_custnum": "BFS123",
    "customer_name": "Bob's Fishing Supplies",
    "po": "PO1234",
    "terms_external_key": "net_60",
    "lines": [
      {
        "prcpart": "PRT TESTPART1",
        "custpart": "TESTPART1",
        "resale": "35.89",
        "cost": "0",
        "qty": 30,
        "revision": "0",
        "description": "",
        "comments": "Lead times (business days) account for any material ordering and/or finishing steps required.",
        "sourcing_comments": "<br>Part viewer URL: <a href=\"https://app.paperlessparts.com/parts/viewer/blah\">View Drawing</a><br>Quote Number: <a href=\"https://app.paperlessparts.com/quotes/edit/1717\">1717</a>",
        "due_date": "2021-09-24",
        "ship_date": "2021-09-21",
        "wip_date": "",
        "external_key": "line_0",
        "transcode": "SA"
      }
    ]
  }
]
```

Integration Deployment Information
----------------------------------

This integration is currently deployed directly on the IOT server at:

    /home/ubuntu/connectors/peredel/peredel

It is scheduled to run every 5 minutes via a crontab job on IOT. If you need to run a test order into the sandbox, there is a test copy of the integration code set up at:

    /home/ubuntu/connectors/peredel/peredel_TEST

The secrets.ini file governs which Paperless Parts user group and Cetec instance will be connected to. In the peredel_TEST directory, you will find secrets_prod2sandbox.ini and secrets_sandbox2sandbox.ini. If you want to run a test order from Prod Paperless Parts to Sandbox Cetec, simply `cp secrets_prod2sandbox.ini secrets.ini` and then call `./run_single_order.sh <order_num>`.

Code Organization
-----------------
The code for this integration predates our class-based approach to integrations. The entry point for running the integration is `connector.py`, which in turn imports the `process_order()` function from `job.py`. The `process_order()` function contains the high-level logic for the integration, which is essentially:
* Loop over the order line items and send the BOM and Routing information for that order line item to Cetec using the /partrevisiondefinition endpoint
* Send the top level order information and a list of line items to the /importjson endpoint

This logic is broken out into helper functions, but it should be relatively straightforward to trace the logic if you need to learn more about the specifics of how the API payloads are constructed.

Contact
-------
Our technical contact at Cetec who has assisted with this integration is:

    Mike Congdon (mike@tech-x.com)

If you have any questions relating to the Cetec API, Mike is the right person to talk to.
