from plex.exporter.processors.base import PlexProcessor
from paperless.objects.orders import OrderComponent, OrderOperation
from plex.objects.part import Part
from baseintegration.datamigration import logger


class PartProcessor(PlexProcessor):

    def get_part_type(self, part_info_op: OrderOperation = None) -> str:
        """
        Get the string value of the costing variable item to use for the part
        type.  If None found use the config default value.

        @param part_info_op : The paperless parts order shop operation that is being used to get PLEX part information
        @type part_info_op : OrderOperation

        @return: The PLEX part type
        @rtype: str
        """
        part_type = None
        if part_info_op:
            part_type = part_info_op.get_variable(self._exporter.erp_config.part_info_costing_variable_part_type)
        if part_type is None:
            part_type = self._exporter.erp_config.default_part_type
        return part_type

    def get_part_group(self, part_info_op: OrderOperation = None) -> str:
        """
        Get the string value of the costing variable item to use for the part
        group.  If None found use the config default value.

        @param part_info_op : The paperless parts order shop operation that is being used to get PLEX part information
        @type part_info_op : OrderOperation

        @return: The PLEX part group
        @rtype: str
        """
        part_group = None
        if part_info_op:
            part_group = part_info_op.get_variable(self._exporter.erp_config.part_info_costing_variable_part_group)
        if part_group is None:
            part_group = self._exporter.erp_config.default_part_group
        return part_group

    def get_part_status(self, part_info_op: OrderOperation = None) -> str:
        """
        Get the string value of the costing variable item to use for the part
        status.  If None found use the config default value.

        @param part_info_op : The paperless parts order shop operation that is being used to get PLEX part information
        @type part_info_op : OrderOperation

        @return: The PLEX part status
        @rtype: str
        """
        part_status = None
        if part_info_op:
            part_status = part_info_op.get_variable(self._exporter.erp_config.part_info_costing_variable_part_status)
        if part_status is None:
            part_status = self._exporter.erp_config.default_part_status
        return part_status

    def get_part_source(self, part_info_op: OrderOperation = None) -> str:
        """
        Get the string value of the costing variable item to use for the part
        source.  If None found use the config default value.

        @param part_info_op : The paperless parts order shop operation that is being used to get PLEX part information
        @type part_info_op : OrderOperation

        @return: The PLEX part source
        @rtype: str
        """
        part_source = None
        if part_info_op:
            part_source = part_info_op.get_variable(self._exporter.erp_config.part_info_costing_variable_part_source)
        if part_source is None:
            part_source = self._exporter.erp_config.default_part_source
        return part_source

    def get_product_type(self, part_info_op: OrderOperation = None) -> str:
        """
        Get the string value of the costing variable item to use for the production
        type.  If None found use the config default value.

        @param part_info_op : The paperless parts order shop operation that is being used to get PLEX part information
        @type part_info_op : OrderOperation

        @return: The PLEX production type
        @rtype: str
        """
        product_type = None
        if part_info_op:
            product_type = part_info_op.get_variable(self._exporter.erp_config.part_info_costing_variable_product_type)
        if product_type is None:
            product_type = self._exporter.erp_config.default_product_type
        return product_type

    def get_building_code(self, part_info_op: OrderOperation = None) -> str:
        """
        Get the string value of the costing variable item to use for the building
        code for inventory.  If None found use the config default value.

        @param part_info_op : The paperless parts order shop operation that is being used to get PLEX part information
        @type part_info_op : OrderOperation

        @return: The PLEX building code
        @rtype: str
        """
        building_code = None
        if part_info_op:
            building_code = part_info_op.get_variable(self._exporter.erp_config.part_info_costing_variable_building_code)
        if building_code is None:
            building_code = self._exporter.erp_config.default_part_building_code
        return building_code

    def _process(self, root_component: OrderComponent, quote_number_with_revision, create=False, lead_days: float = 0) -> Part:

        """
        Create new part in PLEX for Sales Orders
        """

        # TODO: Create purchased components with COMPONENT type

        component = root_component

        # If component has children, process them first
        # After processing, these children will be added to the BOM for this component if necessary
        part_info_operation = None
        for op in root_component.shop_operations:
            if op.operation_definition_name == self._exporter.erp_config.part_information_op_def_name:
                part_info_operation = op

        # TODO: First search to see if the part or rev exists before creating a new one
        part_no = component.part_number if component.part_number is not None else component.part_name.rsplit('.', 1)[0]
        rev = (component.revision if component.revision is not None else '')[:8]
        des = (component.description if component.description is not None else '')[:99]
        existing_parts = Part.find_part(number=part_no, rev=rev)
        matching_parts = [p for p in existing_parts if p.number == part_no and p.revision == rev]
        existing_part = matching_parts[0] if len(matching_parts) > 0 \
            else existing_parts[0] if len(existing_parts) > 0 else None

        lead_time_days = 0
        if lead_days:
            lead_time_days = lead_days
        # If the part and rev match, no need to do anything, we will just reuse the existing
        if existing_part and existing_part.number == part_no and existing_part.revision == rev:
            logger.info(
                'Part {}/Rev {} exists, so will use existing'.format(existing_part.number, existing_part.revision))
            return existing_part
        elif existing_part and existing_part.number == part_no and existing_part.revision != rev:
            new_part = Part(
                number=part_no,
                revision=rev if rev is not None else '',
                name=des,
                standard_job_qty=component.make_quantity,
                bom_substitution_allowed=True,
                type=self.get_part_type(part_info_op=part_info_operation),
                group=self.get_part_group(part_info_op=part_info_operation),
                productType=self.get_product_type(part_info_op=part_info_operation),
                status=self.get_part_status(part_info_op=part_info_operation),
                source=self.get_part_source(part_info_op=part_info_operation),
                note=f'Paperless Parts Quote: https://app.paperlessparts.com/quotes/edit/{quote_number_with_revision}',
                is_new_rev_of_old_part=True,
                buildingCode=self.get_building_code(part_info_op=part_info_operation),
                leadTimeDays=lead_time_days
            )
            logger.info(f'Part {new_part.number} exists, but this is a new rev, so will create a new part')
            if create:
                return new_part.create()
            else:
                return new_part
        else:
            new_part = Part(
                number=part_no,
                revision=rev if rev is not None else '',
                name=des,
                standard_job_qty=component.make_quantity,
                bom_substitution_allowed=True,
                type=self.get_part_type(part_info_op=part_info_operation),
                group=self.get_part_group(part_info_op=part_info_operation),
                productType=self.get_product_type(part_info_op=part_info_operation),
                status=self.get_part_status(part_info_op=part_info_operation),
                source=self.get_part_source(part_info_op=part_info_operation),
                note=f'Paperless Parts Quote: https://app.paperlessparts.com/quotes/edit/{quote_number_with_revision}',
                buildingCode=self.get_building_code(part_info_op=part_info_operation),
                leadTimeDays=lead_time_days
            )
            logger.info('Part {} does not exist. Will make a new part with revision {}'.format(
                new_part.number,
                new_part.revision
            ))
            if create:
                return new_part.create()
            else:
                return new_part
