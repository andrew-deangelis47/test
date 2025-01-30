# Epicor Integration ReadMe

# Configuration Options:

### connection

`plant_code`
* Field type: `string`
* Options: Any string value.
* Default: `None`<br/><br/>

This indicates the specific site/plant that the integration will push to. Useful if you are getting this error message:
`Cannot change the primary production operation at this point.` Not necessary if the shop has one Epicor site.

## Exporters

### orders

`interval`

* Field type: `numeric`
* Options: Any integer value.
* Default: `5`<br/><br/>

This indicates the interval at which the integration will look for new orders to process.

`should_create_customer`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `True`<br/><br/>

This field determines whether the integration will be able to create new customers in Epicor when an existing Epicor
customer cannot be found based on a matching ERP field from a Paperless Parts account. Setting this field to `False`
will result in either:<br/><br/>

* a planned failure (no customer is created and an error message is posted to the integration action), OR
* posting a default customer (see the `default_customer_id` option for more details)

`default_customer_id`

* Field type: `string`
* Options: must be a valid Epicor customer ID or `null` 
* Default: `null` <br/><br/>

In the event that `should_create_customer` is set to `False`, this field will determine whether a default customer is
assigned to the Epicor quote header, or if a planned failure will occur. NOTE: A planed failure will cause the order 
export to fail completely and an error message will be displayed to the user in integration actions instructing them
to create a new customer in Epicor before attempting to reprocess the order.

`new_customer_check_duplicate_po`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `True`<br/><br/>

This is a boolean field that indicates whether the `CheckDuplicatePO` field should be set to True/False when creating a 
new customer in Epicor. This field is irrelevant if creating new customers is disabled.

`new_customer_type`

* Field type: `string`
* Options: 
    * `PRO` - Prospect
    * `CUS` - Customer
    * `SUS` - Suspect
* Default: `PRO`<br/><br/>

This field indicates what new customers should be classified as when created by the integration. There are only three
default options (as listed above). This configuration option is irrelevant if `should_create_customer` is set to
`False`.

`default_payment_terms_code`

* Field type: `numeric`
* Options: There is not a finite list of managed options for this config option.
* Default: `5`<br/><br/>

This field indicates the default payment terms code that will be assigned to a customer when a new customer is created. 
This configuration option is irrelevant if `should_create_customer` is set to `False`.

`should_create_contact`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `True`<br/><br/>

This option indicates whether the integration will create contacts in Epicor. If set to `False`, the integration will
not be able to create new contacts. When set to `True` this feature allows the integration to create contacts in 
Epicor's CRM module.

`should_add_quote_contacts`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `True`<br/><br/>

Enabling this option will allow the integration to create quote contacts. Quote contacts are assigned to the quote
header directly by linking a contact via it's ConNum.

`default_contact_email`

* Field type: `string`
* Options: Must be a valid email address of an existing Epicor customer.
* Default: `test@test.com`<br/><br/>

If the creation of contacts is enabled, this option will have no effect on the integration or the data that is created
in Epicor. If `should_create_contact` is `False`, the integration will attempt to get a default contact using the 
email address specified here.

`should_create_shipping_address`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

Indicates whether a new shipping address should be created and associated with the Epicor customer. If disabled,
no shipping address will be created in Epicor which will result in no shipping information being specified on the
Epicor quote.

`should_mark_quotes_as_quoted`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

This options indiscates whether the quote header should be marked as "quoted". In order for this to be enabled, the 
`should_mark_quotes_as_engineered` configuration option **must be enabled.**

`should_mark_quotes_as_engineered`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

This option indicates whether quote line items should be marked as "engineered". This applies to all line items in a
quote. Quote line items must be marked as "engineered" before the quote header can be marked as "quoted".

`should_mark_quote_lines_as_template`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

This option indicates whether quote line items should be marked as "template". This applies to all line items in a
quote.

`should_add_public_pp_notes_to_quote_detail`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `True`<br/><br/>

Paperless Parts has customer-facing notes and non-customer-facing notes fields. This option indicates whether the
customer-facing notes field should write to the quote comments in Epicor (which is a visible field to Epicor customers).

`should_add_private_pp_notes_to_quote_detail`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

Paperless Parts has customer-facing notes and non-customer-facing notes fields. This option indicates whether the
non-customer-facing notes field should write to the quote comments in Epicor (which is a visible field to Epicor
 customers). This is set to `False` by default because we cannot assume that the private notes in Paperless Parts
 can be displayed on the Epicor quote.

 `should_populate_reference_with_pp_quote_num`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

This option indicates whether the Paperless Parts quote number (and quote revision number if it exists) should be populated within the Epicor "Reference" field, which is a visible field to Epicor customers. This is set to `False` by default because some customers may want to use the "Reference" field to store other information.

`should_add_pp_part_viewer_link_to_quote_comments`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

This option indicates whether a link back to the Paperless Parts part viewer should be populated on the comments for a quote item, which is a visible field to Epicor customers. This is meant to make it easier for Epicor customers to find parts in Paperless. This is set to `False` by default because some customers may not want this URL to show up in the comments section.

`duplicate_part_number_append_character`

* Field type: `string`
* Options: Any string test character or word.
* Default: `CHILD`<br/><br/>

Epicor does not allow any duplicate part numbers to be a parent or child of itself. Paperless Parts does not perform 
any validation to remove duplicate part numbers within an order item, therefore, the integration is responsible for 
removing duplicate part numbers from order items. Instead, duplicate part numbers will be appended with 
"PART-123-CHILD1", "PART-123-CHILD2", etc...

`lead_time_unit_preference`

* Field type: `string`
* Options: `calendar_days`, `business_days`, `calendar_weeks`, `business_weeks`
* Default: `calendar_days`<br/><br/>

Paperless Parts' API only provides lead days in terms of days and does not supply units for the quantity of days listed.
As such, if the lead days represent business days, and the Epicor customer wants their lead time to show up in units of
weeks, the integration needs to know whether to divide by 5, or divide by 7, to get the correct number of weeks. This 
option takes care of that problem.

`default_salesperson_id`

* Field type: `string`
* Options: Any valid salesperson's RapID or EmpID 
* Default: `None`<br/><br/>

Epicor's API is buggy when it comes to adding a salesperson. In ~90% of cases, a Sales Rep Code is not required to 
successfully post a quote header. In some rare cases, Epicor's API will throw an error saying "REST API Exception", 
"ErrorMessage":"A valid SalesRep Code is required". In this case, a Sales Rep Code will be required - it can be 
specified by this config option. You can find a valid sales rep ID in Epicor by going to the Person/Contact 
maintenance, click the Person/Contact button to search, filter by role (Sales Person), and select a contact for this 
purpose. Once selected, locate the RepID, or the EmpID. This value needs to be assigned to this config option.

`set_quote_line_item_prod_code_from_first_pp_op`
* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

Some customers have requested the ability to add line-item-level Product Group Codes. When set to True, this feature 
allows those codes to be set from the first operation in a customer's router. In order to implement this functionality, 
all customer operations will need to have a P3L variable named `epicor_line_item_prod_code` that contains a valid 
Product Group Code as a default, with dropdown options containing the rest of their valid product group codes. Invalid 
product group codes will cause the export to fail.

`set_quote_line_item_sales_code_from_first_pp_op`
* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

Some customers have requested the ability to add line-item-level Sales Codes. When set to True, this feature 
allows those codes to be set from the first operation in a customer's router. In order to implement this functionality, 
all customer operations will need to have a P3L variable named `epicor_line_item_sales_code` that contains a valid 
Sales Code as a default, with dropdown options containing the rest of their valid sales codes. Invalid sales codes will  
cause the export to fail.

`add_ons_should_create_line_items`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

When this field is set to True, the integration exporter will create Paperless Parts Add Ons as additional line items
instead of as MiscCharge items. A single quantity will be created for the each additional Add On line item, where the
quantity is the Add On quantity, and the unit price is the Add On price / quantity.

`default_line_item_add_on_part_number`
* Field type: `string`
* Options: Anything that is a valid Epicor ProdCode (Group ID) for a manufactured/assembled component.
* Default: `PURC`<br/><br/>

This config option allows users to specify a default part number to be associated with a line item add on. This only 
applies when the `add_ons_should_create_line_items` option is set to True. The Paperless Parts add on name will be 
mapped to the Epicor line item description.

`add_ons_should_create_new_misc_charges`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

This option indicates whether the integration will be able to create new MiscCharge objects in Epicor from Paperless 
Parts Add Ons. If this option is set to False, the integration will use the default miscellaneous charge code set in 
the next configuration option below.

`default_misc_charge_code`

* Field type: `string`
* Options: Any valid MiscCharge code/id. 
* Default: `None`<br/><br/>

In the event that the integration is not allowed to create new MiscCharges, this default code will be used in the event 
that a match cannot be found from the Add On name. Note - the exporter will try to get a matching Add On by attempting 
to match the first three letters of the Paperless Add On name with an Epicor MiscCharge (by id). If no match is found 
it will then try to match the Paperless Add On name with an Epicor MiscCharge description. If neither return results, 
it will then either create one, or use the default.

`should_create_raw_materials`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

Indicates whether Epicor part master records will be created from Paperless Parts material operations. If disabled,
part numbers from Paperless Parts material operations that return no matches with existing records in Epicor will not
be created. As a result, the default raw material part number will be assigned in place of the Paperless Parts material
operation part information. (See the next option for more details).

`default_raw_material_id`

* Field type: `string`
* Options: Must be a valid existing Epicor part number.
* Default: `PLACEHOLDER-PART`<br/><br/>

If the creation of raw materials is disabled, this part number will be added to the quote in place of the original 
Paperless Parts material operation part number that was specified on the Paperless Parts quote. In some cases, it may
be advisable to set up a part number to serve this purpose with the Paperless Parts customer. The purpose of this
functionality is to provide the Epicor user with an obvious alert that a part number on the quote needs to be corrected.

`pp_mat_id_variable`

* Field type: `string`
* Options: Must be a valid Paperless Parts material operation variable name available on **all** of this customer's
Paperless Parts material operations.
* Default: `Material ID`<br/><br/>

This option indicates which Paperless Parts material operation variable will be used to pass along an Epicor part number
to the integration. This variable should be available by default on all Paperless Parts customer's accounts that also
have the Epicor integration.

`pp_mat_cost_variable`

* Field type: `string`
* Options: Must be a valid Paperless Parts material operation variable name available on **all** of this customer's
Paperless Parts material operations.
* Default: `unit_cost`<br/><br/>

This option indicates which Paperless Parts material operation variable will be used to pass along the material 
operation's unit cost/price to the integration. This variable should be available by default on all Paperless Parts 
customer's accounts that also have the Epicor integration.

`material_op_quantity_per_parent_var`

* Field type: `string`
* Options: Must be a valid Paperless Parts material operation variable name available on **all** of this customer's
Paperless Parts material operations.
* Default: `quantity_per_parent`<br/><br/>

This option indicates which Paperless Parts material operation variable will be used to pass along the quantity per
parent value of the material operation to the Epicor integration. This variable should be available by default on all 
Paperless Parts customer's accounts that also have the Epicor integration.

`pp_mat_UOMCode_variable`

* Field type: `string`
* Options: Must be a valid Paperless Parts material operation variable name available on **all** of this customer's
Paperless Parts material operations.
* Default: `cost_unit_of_measure`<br/><br/>

This option indicates which Paperless Parts material operation variable will be used to pass along the cost unit of
measure value of the material operation to the Epicor integration. This variable value will only be used to specify the 
cost unit of measure in the event that a new part number is created in Epicor's part master library. This variable 
should be available by default on all Paperless Parts customer's accounts that also have the Epicor integration.

`pp_mat_description_variable`

* Field type: `string`
* Options: Must be a valid Paperless Parts material operation variable name available on **all** of this customer's
Paperless Parts material operations.
* Default: `Material Description`<br/><br/>

This config option indicates what description will be associated with the Epicor part master record when new part
numbers are created. Epicor requires that every part record has a description. If no variable can be found matching
the name specified in the configuration option, then "No Description" will be assigned by default.

`default_raw_material_class_id`

* Field type: `string`
* Options: Must be a valid Epicor part class ID.
* Default: `BAR`<br/><br/>

Indicates what class ID will be assigned when a new Epicor part master record is created from a Paperless Parts 
material operation.

`default_material_op_cost_method`

* Field type: `string`
* Options: `S`, `A`, `L`, `T`
* Default: `S`<br/><br/>

Indicates which cost method will be used when creating new part master records from Paperless Parts material operations. 
The options are the same as listed previously.

`material_op_default_part_type`

* Field type: `string`
* Options: `P`, `M`, `K`, `B`
* Default: `S`<br/><br/>

Indicates the part type that will be used when creating new part master records from Paperless Parts material operations. 
The options are listed here:
* `P` - Purchased
* `M` - Manufactured
* `K` - Kit
* `B` - BOM Planning

`pp_purchased_component_op_def_name`

* Field type: `string`
* Options: Must reference a Paperless Parts operation definition name.
* Default: `PC Piece Price`<br/><br/>

Indicates the name of the purchased component operation that will be used. The integration will look for this operation
on purchased components to then determine the piece price that should be assigned on the Epicor quote.

`pp_purchased_component_op_piece_price_var`

* Field type: `string`
* Options: Must be a valid variable in a Paperless Parts shop operation on the operation definition specified above.
* Default: `piece_price`<br/><br/>

Indicates which variable the integration will use to assign a piece price in Epicor on quote materials.

`default_purchased_comp_cost_method`

* Field type: `string`
* Options: `S`, `A`, `L`, `T`
* Default: `S`<br/><br/>

Indicates which cost method will be used when creating new part master records from Paperless Parts purchased
components. The options are the same as listed previously.

`default_hardware_class_id`

* Field type: `string`
* Options: Must be a valid Epicor part class ID.
* Default: `HDW`<br/><br/>

Indicates what class ID will be assigned when a new Epicor part master record is created from a purchased component
in Paperless Parts.

`set_hardware_components_as_non_stock`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

Indicates whether hardware components will be created in Epicor's part master as "stock" vs.  
"non-stock".

`default_manufactured_class_id`

* Field type: `string`
* Options: Must be a valid Epicor part class ID.
* Default: `MFG`<br/><br/>

Indicates what class ID will be assigned when a new Epicor part master record is created from a manufactured/assembled 
component in Paperless Parts.

`default_manufactured_comp_cost_method`

* Field type: `string`
* Options: `S`, `A`, `L`, `T`
* Default: `S`<br/><br/>

Indicates which cost method will be used when creating new part master records from Paperless Parts manufactured
components. The options stand for the following:
* `S` - standard cost
* `A` - average cost
* `L` - last cost
* `T` - average cost by lot

`default_part_revision`
* Field type: `string`
* Options: Any string character.
* Default: `-`<br/><br/>

If no revision is specified in Paperless Parts, this character will be used to create a revision for the new part 
record in Epcior.

`default_non_root_mfg_product_code`

* Field type: `string`
* Options: Must be a valid Epicor product code
* Default: `MFG`<br/><br/>

Indicates the default product group code when creating new parts in Epicor.

`set_mfg_components_as_non_stock`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

Indicates whether manufactured and assembled components will be created in Epicor's part master as "stock" vs.  
"non-stock".

`pp_op_id_variable`

* Field type: `string`
* Options: Must be a valid Paperless Parts shop operation variable name available on **all** of this customer's
Paperless Parts shop operations.
* Default: `op_code`<br/><br/>

This option is responsible for handling the mapping of a Paperless Parts shop operation to an Epicor operation. The
variable value stored in this field must be a valid Epicor operation code in order towork properly.

`default_operation_id`

* Field type: `string`
* Options: Must be a valid Epicor operation code.
* Default: `99999`<br/><br/>

In the event that the operation code specified in a Paperless Parts shop operation fails to post to Epicor, the 
operation code stored here will be added to the routing step in place of the original code. The purpose of this option 
is to indicate to Epicor users that an operation did not map properly from Paperless Parts to Epicor and some action 
will need to be taken.

`pp_resource_group_id_variable`

* Field type: `string`
* Options: Must be a valid Epicor resource group ID
* Default: `resource_group_id`<br/><br/>

This option indicates which P3L variable will be used to assign a resource group in Epicor. An Epicor operation can 
have a resource group, or individual resource assigned to it. These variables should be available across all shop 
operations that are expected to transfer into Epicor, (ie. everything except "IGNORE" operations).

`pp_resource_id_variable`

* Field type: `string`
* Options: Must be a valid Epicor resource ID (this is different than the resource group id)
* Default: `resource_id`<br/><br/>

This option indicates which P3L variable will be used to assign a specific resource in Epicor. An Epicor operation can 
have a resource group, or individual resource assigned to it. These variables should be available across all shop 
operations that are expected to transfer into Epicor, (ie. everything except "IGNORE" operations).

`default_std_format`

* Field type: `string`
* Options: `HP`, `PH` will likely be the most common. This is a managed list enforced by Epicor.
* Default: `HP`<br/><br/>

This config option indicates the default units that will be assigned to a routing step in Epicor. The options are as 
follows:
* `HP` - Hours/Piece
* `MP` - Minutes/Piece
* `PH` - Pieces/Hour
* `PM` - Pieces/Minute
* `OH` - Operations/Hour
* `OM` - Operations/Minute
* `HR` - Fixed Hours.

`default_std_basis`

* Field type: `string`
* Options: `E` will likely be the most common. This is a managed list enforced by Epicor.
* Default: `HP`<br/><br/>

This config option indicates the standards for time . The options are as 
follows:
* `E` - Eaches
* `C` - 100's
* `M` - 1000's
* `T` - 10,000

`crew_size_variable`
* Field type: `string`
* Options: Any valid P3L variable available in any operation where crew size may apply.
* Default: `crew_size`<br/><br/>

Indicates which P3L variable the integration will look for in order to parse out the crew size value and write it to 
the destination represented in the following configuration option (`crew_size_destination`).

`crew_size_destination`
* Field type: `string`
* Options: `prod`, `setup`, `both`
* Default: `prod`<br/><br/>

Epicor has two fields to capture crew size on each operation, either production or setup. This config option indicates 
to the integration which destination the `crew_size_variable` should write to. If left blank or if this configuration 
option does not exist in your integration, crew sizes will be ignored entirely with no effect, (Epicor will default the 
field to 1).

`pp_vendor_id_variable`
* Field type: `string`
* Options: Must be a P3L variable that captures valid Epicor SupplierIDs, and lives on all outside service operations.
* Default: `SupplierID`<br/><br/>

In order for an operation to be created as "subcontract" operation, Epicor requires a valid SupplierID to be present.
The integration will GET the Epicor Vendor object based on the P3L operation variable and pull the required attributes 
from the vendor instance in order to assign additional parameters on the "QuoteOperation". In the event that the P3L 
vendor id variable is missing, or an invalid vendor ID is specified, the integration will assign the typical default 
operation indicated in the `default_operation_id` configuration option. NOTE: The default operation will be a standard 
non-subcontract operation.

`pp_vendor_unit_cost_variable`
* Field type: `string`
* Options: Must be a P3L variable that captures valid Epicor SupplierIDs, and lives on all outside service operations.
* Default: `SupplierID`<br/><br/>

This variable indicates to the integration which outside service variable should be used to get the unit price for 
subcontract operations. If the variable is not present, the integration will set the unit price to the unit price for 
that specific operation step.

`pp_vendor_lot_charge_variable`
* Field type: `string`
* Options: Must be a P3L variable that captures valid Epicor SupplierIDs, and lives on all outside service operations.
* Default: `SupplierID`<br/><br/>'

This variable indicates to the integration which outside service variable should be used to get the minimum charge/lot 
charge value for subcontract operations.

`pp_mat_op_vendor_num`
* Field type: `string`
* Options: Optional
* Default: `epicor_vendor_num`<br/><br/>'

This is an optional configuration option. It doesn't hurt to have it present, however, if a customer does not typically 
assign an Epicor SupplierID to quote materials, you may leave this variable out of material operations in Paperless. 
If customers do assign SupplierIDs to quote materials, you will need a single P3L variable assigned to all material 
operations in which the customer wants the ability to assign a material vendor. The variable name must be the same 
everywhere. If the variable is not found, no supplier will be added in Epicor (not a big deal).

`pp_mat_op_lead_time`
* Field type: `string`
* Options: Optional
* Default: `epicor_lead_time`<br/><br/>'

This is an optional configuration item. If customers want the lead time field populated when adding a supplier for a 
specific material requirement in Epicor, you will need to implement this config option. This needs to be the same 
variable in all material operations where a supplier ID will be assigned. This field maps to the lead days field 
within Epicor.

`disable_quote_operation_details`
* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>'

In some cases, the cloud based (Epicor Kinetic) version utilizes Epicor's v1 API endpoints for certain behaviors. 
Specifically, quote operation details do not work properly. This configuration disables the abaility for the integration
to update quote operation details. This means a specific resource and/or crew size cannot be assigned when disabled. 

`disable_part_creation`
* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

When part creation is disabled, no records will be created in the part master. "Purchase Direct" 
will be checked for any materials on a quote that do not exist in the part master.


`set_auto_receive_into_inventory_on_last_operation`
* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

Some shops build all of their parts to inventory by default and then fulfill their sales orders directly from 
inventory. This config option indicates to Epicor that upon completing the router for any particular part, it should 
automatically go into inventory. This boolean flag is applied to only the last operation in each router on each 
component.

`set_final_operation_on_last_operation`
* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`<br/><br/>

Similar to the "set_auto_receive_into_inventory_on_last_operation" option, this boolean is applied to only the last 
operation in each router for each component.

`default_root_component_class_id`
* Field type: `string`
* Options: Anything that is a valid Epicor Class ID for a manufactured/assembled component.
* Default: `ROOT`<br/><br/>

This config option represents the default class ID code for root components when creating new Epicor Part records. NOTE:
If a Part with this part number already exists, it will not be updated with this code, this is net new parts only.

`default_root_component_product_code`
* Field type: `string`
* Options: Anything that is a valid Epicor ProdCode for a manufactured/assembled component.
* Default: `ROOT`<br/><br/>

This config option represents the default ProdCode for root components when creating new Epicor Part records. NOTE:
If a Part with this part number already exists, it will not be updated with this code, this is net new parts only.

`default_hardware_product_code`
* Field type: `string`
* Options: Anything that is a valid Epicor ProdCode (Group ID) for a hardware/purchased component.
* Default: `PURC`<br/><br/>

This config option represents the default Group ID or ProdCode value for creating net new hardware components.

`default_non_root_mfg_class_id`
* Field type: `string`
* Options: Anything that is a valid Epicor ProdCode (Group ID) for a manufactured/assembled component.
* Default: `PURC`<br/><br/>

This config option represents the default Group ID or ProdCode value for creating net new manufactured or assembled 
components. This only applies to the root components. You can have a separate Group ID for non-root parts.


## Importers

### materials

`interval`

* Field type: `numeric`
* Options: Any integer value.
* Default: `120`<br/><br/>

This indicates the interval at which the integration will look for new raw materials to process.

`include_raw_material_class_ids`

* Field type: `list` of `string` values
* Options: Must be a YAML list of valid class ids.
* Default: `SHT`, `BAR`<br/><br/>

This config option must be a list of valid Epicor part class ids. The list of ids entered here will represent all the  
material classes that will be treated as raw materials. Epicor does not classify raw materials/purchased components/
manufactured components the way Paperless Parts does. Instead, there's just one part master library containing all 
part numbers, regardless of what they represent. The class IDs indicate that information about the part number. TISs 
will need to work with the customer to determine what class IDs need to be included on this list. Typically, this will 
be all class IDs that represent a raw stock material.

`should_include_null_dates`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `True`<br/><br/>

Determines whether legacy data "null" dates will be captured in the import. Some customers migrated data from older 
versions of Epicor that did not include some newer date fields that the integration relies on to determine when records 
have been updated or changed. When the data was migrated, the date fields were set to `null`. Setting this config 
option to `True` means that every time the importer runs, it will query all the `null` date fields to be reimported 
every time.

`should_update_null_dates`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `True`<br/><br/>

Similar to the last config option, setting this config option to `True` means that today's date will be added to the 
`null` date records so that in the future the integration knows when these part numbers have changed. This improves 
the integration's performance because it will not need to unnecessarily query and import all the (previously) `null` 
records.

`returned_record_limit`

* Field type: `numeric`
* Options: Any integer value.
* Default: `10000`<br/><br/>

Epicor's API uses OData. This config option maps to the `$top` OData filtering mechanism that will limit the number of 
records returned. The first time the importers are run, this should be set to a high number, (like 10,000).

### purchased_components

`interval`

* Field type: `numeric`
* Options: Any integer value.
* Default: `180`<br/><br/>

This indicates the interval at which the integration will look for new purchased components to process.

`should_include_purchased_component_class_ids`

* Field type: `list` of `string` values
* Options: Must be a YAML list of valid class ids.
* Default: `HDW`<br/><br/>

This config option must be a list of valid Epicor part ClassIDs that indicate non-raw material Parts. See the 
`include_raw_material_class_ids` option for more details.

`should_include_null_dates`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `True`<br/><br/>

See the description in the `materials` section for this option. It works the same way.

`should_update_null_dates`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `True`<br/><br/>

See the description in the `materials` section for this option. It works the same way.

`custom_column_header_names`

* Field type: `list` of `string` values
* Options: Must be a YAML list of valid class ids.
* Default: `class_id` - **This option must be present on the list in order for the import to run properly.**<br/><br/>

This configuration option will be used to assembly the column header names that will be available in the purchased 
component module in Paperless Parts. Specifying an additional header here will create an additional header in Paperless 
Parts. NOTE: If you add additional columns, a custom import processor will be required to override the 
`set_custom_paperless_purchased_component_properties` function to add the custom attributes.

`corresponding_column_header_type`

* Field type: `list` of `string` values
* Options: `string`, `numeric`, `boolean`
* Default: `string` - **This option must be present on the list in order for the import to run properly.**<br/><br/>

This config option corresponds with the one above. The first position in this list corresponds to the first position in 
the above list, and so on. This indicates the value type of the column header specified above.

`default_numeric_value`

* Field type: `numeric`
* Options: Any numeric value.
* Default: `0.01`

This option is used to indicate what the default numeric value should be for **all** numeric type fields when importing 
purchased components in the event that a valid value is not found on the Epicor part record.

`default_string_value`

* Field type: `string`
* Options: Any string value.
* Default: `None` NOTE: This is the string word "None", not the absence of a value.

This option is used to indicate what the default string value should be for **all** string type fields when importing 
purchased components in the event that a valid value is not found on the Epicor part record.

`default_boolean_value`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`

This option is used to indicate what the default boolean value should be for **all** boolean type fields when importing 
purchased components in the event that a valid value is not found on the Epicor part record.

`returned_record_limit`

* Field type: `numeric`
* Options: Any integer value.
* Default: `10000`

Epicor's API uses OData. This config option maps to the `$top` OData filtering mechanism that will limit the number of 
records returned. The first time the importers are run, this should be set to a high number, (like 10,000).

`get_pc_price_from_last_cost`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `False`

This option indicates whether the purchased component's piece price should come from 
Costs -> Last Material Cost, rather than Part -> Unit Price.


### accounts:

`interval`

* Field type: `numeric`
* Options: Any integer value.
* Default: `240`<br/><br/>

This indicates the interval at which the integration will look for new customers/contacts/addresses to process.

`import_account_notes`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `True`

Indicates whether the notes associated with customers in Epicor should be imported to the Paperless Parts account.

### work_centers:

`interval`

* Field type: `numeric`
* Options: Any integer value.
* Default: `10080` NOTE: This is done weekly since each time it is a full import of all work centers<br/><br/>

This indicates the interval at which the integration will import all work centers.

`should_import_resource_groups`
  
* Field type: `boolean`
* Options: `True`, `False`
* Default: `True`

Indicates whether a "resource_groups_custom_table" should be created for the resource groups in Epicor in addition to
the standard "work_centers" table.

`should_import_resources`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `True`

Indicates whether a "resources_custom_table" should be created for the individual resources in Epicor in addition to the standard 
"work_centers" table, and/or "resource_groups_custom_table".

`should_map_multi_resource_group`

* Field type: `boolean`
* Options: `True`, `False`
* Default: `True`

Indicates whether an "operation_details_custom_table" should be created that maps resource groups to operations as a many-to-many relation.

### repeat_part:

`interval`

* Field type: `numeric`
* Options: Any integer value.
* Default: `1440` NOTE: This is done weekly since each time it is a full import of all work centers<br/><br/>

This indicates the interval at which the integration will look for updated repeat work.

`import_objects_newer_than`
  
* Field type: `string`
* Options: Any valid date formatted as YYYY-MM-DD
* Default: 2020-01-01

Any jobs, quotes, or ECORevs older than this date will be ignored in repeat work. Everything newer will be imported.
