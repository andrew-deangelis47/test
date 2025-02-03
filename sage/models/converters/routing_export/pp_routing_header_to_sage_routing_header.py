from sage.models.sage_models.routing import RoutingHeader


class PaperlessRoutingHeaderToSageRoutingHeader:
    def to_sage_routing_header(self, pp_routing_header) -> RoutingHeader:

        entity_type = pp_routing_header['entity_type']
        routing = pp_routing_header['routing']
        routing_code = pp_routing_header['routing_code']
        site = pp_routing_header['site']
        header_title = pp_routing_header['header_title']
        use_status = pp_routing_header['use_status']
        valid_from = pp_routing_header['valid_from']
        valid_to = pp_routing_header['valid_to']
        time_unit = pp_routing_header['time_unit']
        wo_management_mode = pp_routing_header['wo_management_mode']
        header_text_0 = pp_routing_header['header_text_0']
        header_text_1 = pp_routing_header['header_text_1']
        header_text_2 = pp_routing_header['header_text_2']
        major_version = pp_routing_header['major_version']
        minor_version = pp_routing_header['minor_version']
        default_rou_code = pp_routing_header['default_rou_code']
        option = pp_routing_header['option']

        sage_routing_header = RoutingHeader()

        sage_routing_header.entity_type = entity_type
        sage_routing_header.routing = routing
        sage_routing_header.routing_code = routing_code
        sage_routing_header.site = site
        sage_routing_header.header_title = header_title
        sage_routing_header.use_status = use_status
        sage_routing_header.valid_from = valid_from
        sage_routing_header.valid_to = valid_to
        sage_routing_header.time_unit = time_unit
        sage_routing_header.wo_management_mode = wo_management_mode
        sage_routing_header.header_text_0 = header_text_0
        sage_routing_header.header_text_1 = header_text_1
        sage_routing_header.header_text_2 = header_text_2
        sage_routing_header.major_version = major_version
        sage_routing_header.minor_version = minor_version
        sage_routing_header.default_rou_code = default_rou_code
        sage_routing_header.option = option

        return sage_routing_header
