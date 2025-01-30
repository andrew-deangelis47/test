from baseintegration.datamigration import logger
from paperless.custom_tables.custom_tables import CustomTable
import math
from baseintegration.utils import safe_get

# Maps to the External Key in Maintenance -> Data Maintenance -> 9TERMS
PAPERLESS_PAYMENT_TERMS_TO_CETEC_PAYMENT_TERMS_MAPPING = {
    'Net 10': 'net_10_c',
    'Net 30': 'net_30_c',
    'Net 45': 'net_45_c',
    'Net 60': 'net_60_c',
    'Net 90': 'net_90_c',
    'COD': 'cod',
    'Credit Card': 'credit_card',
}

# Maps to the External Key in Maintenance -> Data Maintenance -> SHPCDE
PAPERLESS_SHIPPING_TO_CETEC_SHPCDE_MAPPING = {
    'pickup': 'pickup',
    'local_delivery': 'local_delivery',
    'ups_early_am_overnight': 'ups_early_am_overnight',
    'ups_next_day_air': 'ups_next_day_air',
    'ups_second_day_air': 'ups_second_day_air',
    'fedex_second_day_air': 'fedex_second_day_air',
    'fedex_early_am_overnight': 'fedex_early_am_overnight',
    'fedex_next_day_air': 'fedex_next_day_air',
    'fedex_ground': 'fedex_ground',
    'ups_ground': 'ups_ground',
}


def get_paperless_parts_operation_to_cetec_ordline_status_mapping():
    PAPERLESS_OPERATION_TO_CETEC_LOCATION_OPERATION_MAPPING = {}
    try:
        sales_id_mapping_table_details = CustomTable.get('operation_to_work_center_mapping')
        rows = sales_id_mapping_table_details['rows']
        for row in rows:
            val = row['cetec_ordline_status_external_key']
            PAPERLESS_OPERATION_TO_CETEC_LOCATION_OPERATION_MAPPING[row['paperless_parts_operation_name']] = val

    except Exception as e:
        logger.error(f'Encountered an error fetching the operation to work center mapping: {e}')
    return PAPERLESS_OPERATION_TO_CETEC_LOCATION_OPERATION_MAPPING


def assemble_routing_data_for_component(erp_config, component, quantity, paperless_operation_to_cetec_location_operation_mapping):
    locations = []
    op_counter = 0

    if component.type == 'purchased':
        return locations

    ordline_status_counter = 0
    for op in component.shop_operations:
        # These operations do not correspond to work centers in the shop
        if op.name == 'Production Volume':  # Note - there are two ops whose P3L changes their name to 'Production Volume' - in this case we actually do want to use op.name
            continue
        if op.operation_definition_name is not None and op.operation_definition_name.startswith('Part Complexity'):
            continue
        if op.operation_definition_name is not None and op.operation_definition_name.startswith('Customer Part Number'):
            continue

        # Try to find the operation name first, but if that isn't found check the operation definition name
        external_key = paperless_operation_to_cetec_location_operation_mapping.get(op.operation_definition_name, erp_config.default_work_center)
        logger.info(f"external key is {external_key}")
        if external_key is None:
            continue

        op_notes = op.notes
        if op_notes is not None and op_notes.startswith(
                'Local Delivery |'):  # We use the operation notes to indicate if local delivery is needed, don't show this in the notes in Cetec
            op_notes = op_notes.replace('Local Delivery |', '')
        instructions = [{'instruction': op_notes}] if op_notes is not None else []

        # If this is an outside operation, we need to use Cetec's lead_time and make sure not to set repetitions
        # or setup on the build operation
        if op.is_outside_service:
            ordered_quantity_data = [q for q in op.quantities if q.quantity == quantity]
            try:
                oq = ordered_quantity_data[0]
                lead_time = oq.manual_lead_time if oq.manual_lead_time is not None else oq.lead_time
            except IndexError:
                lead_time = 0
            location_data = {
                "location_external_key": external_key,
                "build_order": ordline_status_counter + 1,
                "lead_time": lead_time,
                # "operations": {
                #     "operation_external_key": 'generic_1_sec_operation',
                #     "instructions": instructions
                # }  # In his email dated 5/19/2020, Mike Congdon said I might be able to include an operation on an outsource location, but I tried and it didn't work
            }
            locations.append(location_data)
            continue

        cetec_build_ops = []
        setup_time = op.setup_time if op.setup_time is not None else 0
        if setup_time > 0:
            op_counter += 1
            cetec_build_ops.append(
                {
                    "operation_external_key": 'generic_1_sec_operation',
                    "repetitions": int(setup_time * 60 * 60),  # convert to seconds
                    "setup": True,
                    "place_in_line": op_counter,
                    "instructions": instructions
                }
            )
        runtime = op.runtime if op.runtime is not None else 0
        if runtime > 0:
            op_counter += 1
            cetec_build_ops.append(
                {
                    "operation_external_key": 'generic_1_sec_operation',
                    "repetitions": int(runtime * 60 * 60),  # convert to seconds
                    "setup": False,
                    "place_in_line": op_counter,
                    "instructions": instructions
                }
            )
        # If neither setup nor runtime is set, create a build operation anyway to pass in the instructions
        if not cetec_build_ops:
            op_counter += 1
            cetec_build_ops.append(
                {
                    "operation_external_key": 'generic_1_sec_operation',
                    "repetitions": 1,
                    "setup": False,
                    "place_in_line": op_counter,
                    "instructions": instructions
                }
            )

        location_data = {
            "location_external_key": external_key,
            "build_order": ordline_status_counter + 1,
            "operations": cetec_build_ops
        }
        locations.append(location_data)

        ordline_status_counter += 1
    return locations


def assemble_material_sourcing_comments(component, material_op, material_name):  # noqa: C901 ; pragma: no cover
    material_sourcing_comments = ''

    costing_variables = None
    material_geometry = None
    if component.material_operations:
        costing_variables = material_op.costing_variables
        material_geometry = material_op.operation_definition_name
    qty_per_top = None
    part_length_in = None
    cutoff_in = None
    material_diameter_in = None
    if costing_variables is not None:
        costing_variables = {var.label: var for var in costing_variables}

        bar_length_in_var = costing_variables.get('Bar Length, in', None)
        part_length_in_var = costing_variables.get('Part Length, in', None)
        cutoff_in_var = costing_variables.get('Cutoff, in', None)
        parts_per_bar_var = costing_variables.get('Parts Per Bar', None)
        material_diameter_var = costing_variables.get('Material Diameter, in', None)
        sheet_width_in_var = costing_variables.get('Sheet Width, in', None)
        sheet_length_in_var = costing_variables.get('Sheet Length, in', None)
        material_thickness_in_var = costing_variables.get('Material Thickness, in', None)
        parts_per_sheet_var = costing_variables.get('Parts Per Sheet', None)

        if material_diameter_var is not None:
            material_diameter_in = material_diameter_var.value

        if not any([x is None for x in [bar_length_in_var, part_length_in_var, cutoff_in_var, parts_per_bar_var]]):
            bar_length_in = bar_length_in_var.value
            part_length_in = part_length_in_var.value
            cutoff_in = cutoff_in_var.value

            # Compute the derived values
            qty_per_top = part_length_in + cutoff_in

            net_qty_need = qty_per_top * component.deliver_quantity

            if bar_length_in > 0:
                net_qty_need_in_bars = net_qty_need / bar_length_in
            else:
                net_qty_need_in_bars = 0.

            net_qty_need_in_bars_whole = int(math.ceil(net_qty_need_in_bars))

            net_qty_whole = net_qty_need_in_bars_whole * bar_length_in

            # Add the relevant values to the sourcing comments
            material_sourcing_comments = f'{material_sourcing_comments}<br>Supplier Section:'
            material_sourcing_comments = f'{material_sourcing_comments}<br>Material Name: {material_name}'
            material_sourcing_comments = f'{material_sourcing_comments}<br>Bar Length: {bar_length_in:.3f} in'
            # material_sourcing_comments = f'{material_sourcing_comments}<br>Number of Bars: {num_bars}'
            if material_diameter_in is not None:
                material_sourcing_comments = f'{material_sourcing_comments}<br>Diameter: {material_diameter_in:.3f} in'
            material_sourcing_comments = f'{material_sourcing_comments}<br>Net Qty Need In Bars (Whole): {net_qty_need_in_bars_whole}'
            material_sourcing_comments = f'{material_sourcing_comments}<br>Net Qty Need (Whole): {net_qty_whole:.3f} in'
            if material_geometry is not None:
                material_sourcing_comments = f'{material_sourcing_comments}<br>Material Geometry: {material_geometry}'

            material_sourcing_comments = f'{material_sourcing_comments}<br><br>Internal Section:'
            material_sourcing_comments = f'{material_sourcing_comments}<br>Qty Per Top: {qty_per_top:.3f} in'
            material_sourcing_comments = f'{material_sourcing_comments}<br>Net Qty Need: {net_qty_need:.3f} in'
            material_sourcing_comments = f'{material_sourcing_comments}<br>Net Qty Need In Bars: {net_qty_need_in_bars:.3f}'

        if not any([x is None for x in [sheet_width_in_var, sheet_length_in_var,
                                        parts_per_sheet_var]]):  # Exclude material_thickness_in_var to preserve backwards compatibility with ops from before that var was added
            sheet_width_in = sheet_width_in_var.value
            sheet_length_in = sheet_length_in_var.value
            material_thickness_in = safe_get(material_thickness_in_var, 'value')
            parts_per_sheet = parts_per_sheet_var.value

            if parts_per_sheet > 0:
                num_sheets = math.ceil(float(component.deliver_quantity) / parts_per_sheet)
            else:
                num_sheets = 0

            # Add the relevant values to the sourcing comments
            material_sourcing_comments = f'{material_sourcing_comments}<br>Material Name: {material_name}'
            material_sourcing_comments = f'{material_sourcing_comments}<br>Sheet Width: {sheet_width_in:.3f} in'
            material_sourcing_comments = f'{material_sourcing_comments}<br>Sheet Length: {sheet_length_in:.3f} in'
            if material_thickness_in is not None:
                material_sourcing_comments = f'{material_sourcing_comments}<br>Material Thickness: {material_thickness_in:.3f} in'
            material_sourcing_comments = f'{material_sourcing_comments}<br>Number of Sheets: {num_sheets}'
    if material_geometry is not None:
        material_sourcing_comments = f'{material_sourcing_comments}<br>Material Geometry: {material_geometry}'
    return cutoff_in, material_sourcing_comments, part_length_in, qty_per_top


def extract_raw_material_prcpart(material_name, material_op):
    raw_material_prcpart = f'RAW{material_name}'
    costing_vars = {var.label: var for var in material_op.costing_variables}
    if 'Material Code' in costing_vars:
        raw_material_prcpart = costing_vars['Material Code'].value
    return raw_material_prcpart


def assemble_raw_material_json(component):
    raw_material_bom_definition = None
    if component.material is not None and component.material_operations:
        # Assume that the first material operation has the information we need
        material_op = component.material_operations[0]
        material_name = component.material.name

        cutoff_in, material_sourcing_comments, part_length_in, qty_per_top = assemble_material_sourcing_comments(
            component, material_op, material_name)

        raw_material_prcpart = extract_raw_material_prcpart(material_name, material_op)

        raw_material_bom_definition = {
            "component": 1,
            "prcpart": raw_material_prcpart,
            "sourcing": material_sourcing_comments,
            "pick_comments": f"Part Length, In (for job): {part_length_in} || Cutoff, In (for job): {cutoff_in}",
            "qty_per_top": qty_per_top,
        }

    return raw_material_bom_definition


def assemble_placeholder_raw_material_json(component):
    raw_material_bom_definition = {
        "component": 1,
        "prcpart": 'RAW FIXME',
        "sourcing": '',
        "pick_comments": '',
        "qty_per_top": 1,
    }

    return raw_material_bom_definition
