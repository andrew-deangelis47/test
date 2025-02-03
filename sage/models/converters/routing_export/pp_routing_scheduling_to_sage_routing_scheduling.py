from sage.models.sage_models.routing import RoutingScheduling


class PaperlessRoutingSchToSageRoutingSch:
    def to_sage_routing_sch(self, pp_routing_scheduling) -> RoutingScheduling:

        entity_type = pp_routing_scheduling['entity_type']
        operation = pp_routing_scheduling['operation']
        downstream_operation = pp_routing_scheduling['downstream_operation']
        milestone = pp_routing_scheduling['milestone']
        production_step = pp_routing_scheduling['production_step']
        scheduling = pp_routing_scheduling['scheduling']
        overlapping_time = pp_routing_scheduling['overlapping_time']
        overlapping_qty = pp_routing_scheduling['overlapping_qty']
        number_of_overlap_lots = pp_routing_scheduling['number_of_overlap_lots']

        sage_routing_scheduling = RoutingScheduling()

        sage_routing_scheduling.entity_type = entity_type
        sage_routing_scheduling.operation = operation
        sage_routing_scheduling.downstream_operation = downstream_operation
        sage_routing_scheduling.milestone = milestone
        sage_routing_scheduling.production_step = production_step
        sage_routing_scheduling.scheduling = scheduling
        sage_routing_scheduling.overlapping_time = overlapping_time
        sage_routing_scheduling.overlapping_qty = overlapping_qty
        sage_routing_scheduling.number_of_overlap_lots = number_of_overlap_lots

        return sage_routing_scheduling
