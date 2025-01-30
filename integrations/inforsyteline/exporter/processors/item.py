from baseintegration.exporter import BaseProcessor, logger
from paperless.objects.orders import Order, OrderItem, OrderComponent
from inforsyteline.utils import ItemData, MaterialData, get_part_number_and_name, ItemProcessorData
from inforsyteline.models import ItemMst, ProdcodeMst, JobMst
from django.db import connection


class ItemProcessor(BaseProcessor):

    def _process(self, order: Order) -> ItemProcessorData:
        logger.info("Processing items -- manufactured components, purchased components, and materials")
        self.order = order
        self.manufactured_components = []
        self.purchased_components = []
        self.materials = []
        logger.info("Iterating through each order item")
        # for each order item, iterate through all components and create a part if necessary
        for item in order.order_items:
            self.get_parts_and_materials(item)
        return ItemProcessorData(manufactured_components=self.manufactured_components,
                                 purchased_components=self.purchased_components,
                                 materials=self.materials)

    def get_parts_and_materials(self, item: OrderItem) -> None:
        for component in item.components:
            logger.info(f"Checking component {component.part_name}")
            part: ItemData = self.get_or_create_item(component, item)
            if part.component.is_hardware:
                logger.info(f"Item {part.item_number} is a purchased component, going into purchased component list")
                self.purchased_components.append(part)
            else:
                logger.info(f"Item {part.item_number} is a manufactured component, going into mfg component list")
                self.manufactured_components.append(part)
            # check if part is new. If yes, add its materials to the list
            if part.item_is_new:
                self.get_materials(component)

    def get_materials(self, component: OrderComponent) -> None:
        logger.info(f"Len of material operations is {len(component.material_operations)}")
        for material in component.material_operations:
            # skip the manual operations that are added to material operations
            if "Manual Operation" not in material.name.title():
                logger.info(f"Material {material.name} found, adding to materials list")
                if material.get_variable("Item") is None or material.get_variable("Item") == "Item No.":
                    logger.info(f"No material lookup for {material.name}, this must be an informational operation")
                    continue
                found_material: ItemData = self.get_or_create_item(material)
                # swizzle in component rather than orderoperation
                found_material = found_material._replace(component=component)
                self.materials.append(MaterialData(part_data=found_material, material_op=material))

    def get_or_create_item(self, component, item: OrderItem) -> ItemData:
        part_number, part_name = get_part_number_and_name(component)
        logger.info(f"Checking for part with part number {str(part_number)}")
        part_number = str(part_number)[0:30]
        if hasattr(component, 'shop_operations'):
            operations = list(component.shop_operations)
        else:
            operations = []
        part = ItemMst.objects.filter(item=part_number).first()
        part_is_new = False
        # if part does not exist yet based on part number, create it in inforsyteline
        if not part:
            part_is_new = True
            logger.info(f"Item not found, creating item with item number {str(part_number)}")
            product_code = self._exporter.erp_config.default_product_code
            code = "P"
            cost_type = "A"
            cost_method = "A"
            revision = None
            if hasattr(component, 'description'):
                description = component.description
            else:
                description = part_number
            if hasattr(component, 'make_quantity'):
                qty = component.make_quantity
            else:
                qty = 1
            if isinstance(component, OrderComponent) and not component.is_hardware:
                code = "M"
                cost_type = "S"
                cost_method = "S"
                if component.revision:
                    revision = component.revision
            # we have to use SQL sps in order to write to Syteline but cannot use them for testing
            if not self._exporter._integration.test_mode:
                with connection.cursor() as cursor:
                    sql = f"""
                    SET NOCOUNT ON;
                    DECLARE @RC int;
                    DECLARE	@Infobar InfobarType;
                    Exec [{self._exporter.erp_config.name}].[dbo].[SetSiteSp] '{self._exporter.erp_config.site_ref}', Infobar
                    EXEC @RC = [{self._exporter.erp_config.name}].[dbo].[CreateItemSp]
                    @Item='{part_number}',
                    @Description='{description}',
                    @Revision='{revision}',
                    @UM='EA',
                    @ProductCode='{product_code}',
                    @Job=NULL,
                    @Suffix=NULL,
                    @JobType='J',
                    @Infobar=@Infobar OUTPUT;
                    UPDATE [{self._exporter.erp_config.name}].[dbo].[item_mst]
                    SET [p_m_t_code] = '{code}', [lot_size] = '{qty}', [cost_type] = '{cost_type}', [cost_method] = '{cost_method}', [issue_by] = 'LOC', [pass_req] = 1, [accept_req] = 1, [lot_tracked] = 0
                    WHERE [Item] = '{part_number}'
                    SELECT @Infobar as N'@Infobar'
                    """
                    cursor.execute(sql)
                    try:
                        # log error message if appropriate
                        logger.info(cursor.fetchone()[0])
                    except:
                        pass
            else:
                import random
                item = ItemMst.objects.create(item=part_number,
                                              description=part_name,
                                              product_code=ProdcodeMst.objects.filter(product_code=product_code).first(),
                                              cost_type=cost_type,
                                              cost_method=cost_method)
                # add corresponding job for item
                job_num = "TEST" + str(random.randint(1, 1000000000))
                JobMst.objects.create(site_ref="SYTE", type="S", job=job_num, item=part_number)
                item.job = job_num
                item.save()
            logger.info("Item was created")
            item = ItemMst.objects.filter(item=part_number)
            if not item:
                raise ValueError("Item was not created")
        else:
            logger.info(f"Item {part_number} found, do not need to create a new item")
        return ItemData(item_number=part_number, component=component, item_is_new=part_is_new, routing_operations=operations)
