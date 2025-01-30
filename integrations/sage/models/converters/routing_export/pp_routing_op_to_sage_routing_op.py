from sage.models.sage_models.routing import RoutingOp


class PaperlessRoutingOpToSageRoutingOp:
    def to_sage_routing_op(self, pp_routing_op) -> RoutingOp:
        entity_type = pp_routing_op['entity_type']
        operation = pp_routing_op['operation']
        alternate_index = pp_routing_op['alternate_index']
        start_date = pp_routing_op['start_date']
        end_date = pp_routing_op['end_date']
        standard_op = pp_routing_op['standard_op']
        main_work_center = pp_routing_op['main_work_center']
        labor_work_center = pp_routing_op['labor_work_center']
        labor_time_set_fac = pp_routing_op['labor_time_set_fac']
        labor_r_time_fact = pp_routing_op['labor_r_time_fact']
        ope_description = pp_routing_op['ope_description']
        operation_uom = pp_routing_op['operation_uom']
        stk_ope_converstion = pp_routing_op['stk_ope_converstion']
        number_of_resources = pp_routing_op['number_of_resources']
        number_labor_res = pp_routing_op['number_labor_res']
        percent_efficiency = pp_routing_op['percent_efficiency']
        shrinkage_in_percentage = pp_routing_op['shrinkage_in_percentage']
        run_time_code = pp_routing_op['run_time_code']
        management_unit = pp_routing_op['management_unit']
        base_quantity = pp_routing_op['base_quantity']
        preparation_time = pp_routing_op['preparation_time']
        setup_time = pp_routing_op['setup_time']
        run_time = pp_routing_op['run_time']
        rate = pp_routing_op['rate']
        waiting_time = pp_routing_op['waiting_time']
        post_run_time = pp_routing_op['post_run_time']
        subcontract = pp_routing_op['subcontract']
        subcontract_prod = pp_routing_op['subcontract_prod']
        operation_text_1 = pp_routing_op['operation_text_1']
        operation_text_2 = pp_routing_op['operation_text_2']
        operation_text_3 = pp_routing_op['operation_text_3']

        sage_routing_op = RoutingOp()

        sage_routing_op.entity_type = entity_type
        sage_routing_op.operation = operation
        sage_routing_op.alternate_index = alternate_index
        sage_routing_op.start_date = start_date
        sage_routing_op.end_date = end_date
        sage_routing_op.standard_op = standard_op
        sage_routing_op.main_work_center = main_work_center
        sage_routing_op.labor_work_center = labor_work_center
        sage_routing_op.labor_time_set_fac = labor_time_set_fac
        sage_routing_op.labor_r_time_fact = labor_r_time_fact
        sage_routing_op.ope_description = ope_description
        sage_routing_op.operation_uom = operation_uom
        sage_routing_op.stk_ope_conversion = stk_ope_converstion
        sage_routing_op.number_of_resources = number_of_resources
        sage_routing_op.number_labor_res = number_labor_res
        sage_routing_op.percent_efficiency = percent_efficiency
        sage_routing_op.shrinkage_in_percentage = shrinkage_in_percentage
        sage_routing_op.run_time_code = run_time_code
        sage_routing_op.management_unit = management_unit
        sage_routing_op.base_quantity = base_quantity
        sage_routing_op.preparation_time = preparation_time
        sage_routing_op.setup_time = setup_time
        sage_routing_op.run_time = run_time
        sage_routing_op.rate = rate
        sage_routing_op.waiting_time = waiting_time
        sage_routing_op.post_run_time = post_run_time
        sage_routing_op.subcontract = subcontract
        sage_routing_op.subcontract_prod = subcontract_prod
        sage_routing_op.operation_text_1 = operation_text_1
        sage_routing_op.operation_text_2 = operation_text_2
        sage_routing_op.operation_text_3 = operation_text_3

        return sage_routing_op
