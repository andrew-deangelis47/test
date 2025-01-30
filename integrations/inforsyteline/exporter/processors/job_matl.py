from baseintegration.exporter import BaseProcessor, logger
from paperless.objects.orders import OrderComponent, OrderOperation
from inforsyteline.utils import MaterialData, ItemData
from inforsyteline.models import ItemMst, JobrouteMst, JobmatlMst
from django.db import connection


class JobMatlProcessor(BaseProcessor):

    def _process(self, manufactured_components, purchased_components, materials) -> None:
        logger.info("Processing job materials")
        self.materials = materials
        self.purchased_components = purchased_components
        self.manufactured_components = manufactured_components
        self.sequence = 0
        for manufactured_comp in manufactured_components:
            if manufactured_comp.item_is_new:
                manufactured_comp: ItemData = manufactured_comp
                m_comp: OrderComponent = manufactured_comp.component
                self.sequence = 0
                self.add_materials_to_bom(m_comp, manufactured_comp)
                self.add_child_components_to_bom(m_comp, manufactured_comp)
                for op in m_comp.shop_operations:
                    if op.operation_definition_name and "outside process" in op.operation_definition_name.lower():
                        self.create_outside_service_item(manufactured_comp.item_number, op)
            else:
                logger.info(f"Item {manufactured_comp.item_number} is not new, not creating job requirements")

    def add_child_components_to_bom(self, m_comp: OrderComponent, manufactured_comp: ItemData):
        assembly_op_no = self.get_assembly_op_no(manufactured_comp.item_number)
        hardware_op_no = self.get_hardware_op_no(manufactured_comp.item_number)
        for child_id in m_comp.child_ids:
            item_data: ItemData = self.get_matching_item_data(child_id)
            if item_data:
                if item_data.component.is_hardware:
                    selected_op_no = hardware_op_no
                else:
                    selected_op_no = assembly_op_no
                self.sequence += 1
                self.add_item(manufactured_comp.item_number, item_data, selected_op_no)

    def add_materials_to_bom(self, m_comp: OrderComponent, manufactured_comp: ItemData):
        for material_op in m_comp.material_operations:
            material_data: MaterialData = self.get_matching_material_op(material_op.id)
            if material_data:
                material_op_no = self.get_material_op_no(manufactured_comp.item_number, material_op)
                self.add_material(manufactured_comp.item_number, material_data.part_data.item_number, material_op, material_op_no)
                self.sequence += 1

    def create_outside_service_item(self, parent_item_number: str, operation: OrderOperation):
        # optionally override this
        pass

    def get_assembly_op_no(self, item_number: str) -> int:
        assembly_op_no = 10
        logger.info(f"Checking item number {item_number} for an assembly op no")
        job = ItemMst.objects.filter(item=item_number).first().job
        job_operations = JobrouteMst.objects.filter(job=job)
        for op in job_operations:
            op: JobrouteMst = op
            if op.wc and op.wc.description and "assembly" in op.wc.description.lower():
                return op.oper_num
        else:
            return assembly_op_no

    def get_hardware_op_no(self, item_number: str) -> int:
        return 10

    def get_material_op_no(self, item_number: str, material_op: OrderOperation):
        return 10

    def get_material_qty(self, material_op: OrderOperation):
        return material_op.get_variable("Pounds Of Paint Per Material")

    def get_material_um(self, material_op: OrderOperation):
        return "LB"

    def get_material_cost(self, material_op: OrderOperation):
        return material_op.get_variable("Paint Material Cost")

    def add_material(self, parent_item_number: str, child_item_number: str, material_op: OrderOperation, selected_op_no: int) -> None:
        pass

    def add_item(self, parent_item_number: str, item_data: ItemData, selected_op_no: int) -> None:
        logger.info(f"Attempting to add job matl {item_data.item_number} with parent {parent_item_number}")
        qty = item_data.component.make_quantity
        if not self._exporter._integration.test_mode:
            with connection.cursor() as cursor:
                sql = f"""
                SET NOCOUNT ON;
                DECLARE @RC int;
                DECLARE @myid uniqueidentifier;
                DECLARE	@Infobar InfobarType;
                SET @myid = NEWID();
                Exec [{self._exporter.erp_config.name}].[dbo].[SetSiteSp] '{self._exporter.erp_config.site_ref}', Infobar
                EXEC @RC = [{self._exporter.erp_config.name}].[dbo].[CreateCurrentMaterialSp]
                 @Item='{parent_item_number}'
                 , @CreateNonInventoryItems='0'
                 , @JobmatlOperNum='{selected_op_no}'
                 , @JobmatlSequence='{self.sequence}'
                 , @JobmatlBomSeq=NULL
                 , @JobmatlMatlType='M'
                 , @JobmatlItem='{item_data.item_number}'
                 , @JobmatlUM='EA'
                 , @JobmatlDescription=NULL
                 , @JobmatlRefType='I'
                 , @JobmatlUnits='U'
                 , @JobmatlScrapFact='0'
                 , @JobmatlFmatlovhd='0'
                 , @JobmatlVmatlovhd='0'
                 , @JobmatlMatlQty='{qty}'
                 , @JobmatlCost='0'
                 , @JobmatlMatlCost='0'
                 , @JobmatlLbrCost='0'
                 , @JobmatlFovhdCost='0'
                 , @JobmatlVovhdCost='0'
                 , @JobmatlOutCost='0'
                 , @JobmatlEffectDate=NULL
                 , @JobmatlObsDate=NULL
                 , @JobmatlBackflush='0'
                 , @JobmatlBflushLoc=NULL
                 , @JobmatlAltGroup='1'
                 , @JobmatlAltGroupRank='0'
                 , @JobmatlPlannedAlternate='0'
                 , @JobmatlIncPrice=NULL
                 , @JobmatlManufacturerId=NULL
                 , @JobmatlManufacturerItem=NULL
                 , @JobmatlFeature=NULL
                 , @JobmatlOptCode=NULL
                 , @JobmatlProbable=NULL
                 , @JobmatlRowPointer=@myid
                 , @Infobar=@Infobar OUTPUT;
                 SELECT @Infobar as N'@Infobar';
                """
                cursor.execute(sql)
                try:
                    # log error message if appropriate
                    logger.info(cursor.fetchone()[0])
                except:
                    pass
        else:
            item_job = ItemMst.objects.filter(item=item_data.item_number).first().job
            JobmatlMst.objects.create(
                site_ref="SYTE",
                job=item_job,
                oper_num=selected_op_no,
                sequence=self.sequence,
                item=item_data.item_number,
                matl_qty=qty
            )
        logger.info("Material item added!")

    def get_matching_item_data(self, child_id: int):
        for potential_comp in self.manufactured_components:
            potential_comp: ItemData = potential_comp
            if potential_comp.component.id == child_id:
                return potential_comp
        for potential_comp in self.purchased_components:
            potential_comp: ItemData = potential_comp
            if potential_comp.component.id == child_id:
                return potential_comp
        return None

    def get_matching_material_op(self, mat_op_id: int) -> MaterialData:
        for material in self.materials:
            material: MaterialData = material
            if material.material_op.id == mat_op_id:
                return material
