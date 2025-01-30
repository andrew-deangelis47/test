from attr import attr
from attr.validators import optional, instance_of
from baseintegration.datamigration import logger
from sage.models.sage_models import BaseFullEntityObject
from sage.models.sage_models.routing import RoutingOp, RoutingScheduling, RoutingHeader


class RoutingFullEntity(BaseFullEntityObject):

    # according to the import/export template for ZROUT it goes header => op => scheduling which is the order of the
    # sections on the routing page

    def get_routing_header_and_routing_op_and_routing_sheduling_return_full_routing(self, routing_header, routing_operations,
                                                                                    routing_schedulings):

        complete_routing_i_file = '' + routing_header.to_i_file()

        if len(routing_operations) > 1:
            logger.info('more then on operation to process')
            for op in routing_operations:
                op = op.to_i_file()
                complete_routing_i_file += op
        else:
            logger.info('1 route op to process')
            if len(routing_operations) > 0:
                op = routing_operations[0].to_i_file()
                complete_routing_i_file += op

        if len(routing_schedulings) > 1:
            logger.info('more then on route schedule to process')
            for sch in routing_schedulings:
                sch = sch.to_i_file()
                complete_routing_i_file += sch
        else:
            logger.info('1 route schedule to process')
            if len(routing_schedulings) > 0:
                sch = routing_schedulings[0].to_i_file()
                complete_routing_i_file += sch

        complete_routing_i_file += 'END'
        complete_routing_i_file_replace_semis_with_commas = complete_routing_i_file.replace(';', ',')
        return complete_routing_i_file_replace_semis_with_commas

    def __init__(self, routing_details: RoutingHeader = None, routing_op: RoutingOp = None,
                 routing_scheduling: RoutingScheduling = None):
        self.routing_details = routing_details
        self.routing_op = routing_op
        self.routing_scheduling = routing_scheduling

    routing_header = attr.ib(validator=optional(instance_of(RoutingHeader)), default=None)
    routing_op = attr.ib(validator=optional(instance_of(RoutingOp)), default=None)
    routing_scheduling = attr.ib(validator=optional(instance_of(RoutingScheduling)), default=None)

    def to_i_file(self):
        return self.routing_header.to_i_file() + self.routing_op.to_i_file() + self.routing_scheduling.to_i_file() + 'END'
