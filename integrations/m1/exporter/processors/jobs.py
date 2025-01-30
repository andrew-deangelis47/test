from baseintegration.datamigration import logger
from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.orders import Order, OrderItem, OrderOperation, OrderComponent
from m1.exporter.processors.utils import NoteUtils, PartUtils
from m1.models import Jobs, Salesorderlines, Salesorders, Joboperations, Salesorderjoblinks, Jobassemblies, \
    Jobmaterials, Workcenters, Processes


class ProcessJobs(BaseProcessor):

    def _process(self, order: Order, new_sales_order: Salesorders, new_sales_order_line: Salesorderlines,
                 item: OrderItem, idx: int):
        logger.info(f'Start job creation for order {order.number}')
        job_id = f'{new_sales_order_line.omlsalesorderid}-{new_sales_order_line.omlsalesorderlineid}'
        line_item_notes = NoteUtils.get_line_item_notes(item=item)
        job: Jobs = Jobs.objects.create(
            jmpjobid=job_id,
            jmpcustomerorganizationid=new_sales_order.ompcustomerorganizationid,
            jmppartid=new_sales_order_line.omlpartid,
            jmppartrevisionid=new_sales_order_line.omlpartrevisionid,
            jmppartwarehouselocationid='MAIN',  # TODO Hardcode Alert
            jmppartbinid='NONE',  # TODO Hardcode Alert
            jmpunitofmeasure='EA',  # TODO Hardcode Alert
            jmppartshortdescription=new_sales_order_line.omlpartshortdescription,
            jmppartlongdescriptionrtf=new_sales_order_line.omlpartlongdescriptionrtf,
            jmppartlongdescriptiontext=new_sales_order_line.omlpartlongdescriptiontext,
            jmpproductionnotestext=line_item_notes,
            jmpproductionnotesrtf=line_item_notes,
            jmporderquantity=item.root_component.deliver_quantity,
            jmpinventoryquantity=0.0000,
            jmpscrapquantity=item.root_component.make_quantity - item.root_component.deliver_quantity,
            jmpreworkquantity=0.0000,
            jmpproductionquantity=item.root_component.make_quantity,
            jmpproductionduedate=order.ships_on_dt,
            jmpfirm=False,
            jmptimeandmaterial=False,
            jmpplanningcomplete=False,
            jmpschedulecomplete=False,
            jmpschedulelocked=False,
            jmpreleasedtofloor=False,
            jmponhold=False,
            jmpreadytoprint=False,
            jmpproductioncomplete=False,
            jmpquantitycompleted=0.0000,
            jmpquantityshipped=0.0000,
            jmpquantityreceivedtoinventory=0.0000,
            jmpquotelineid=0,
            jmprmaclaimlineid=0,
            jmpclosed=False,
            jmpscrapquantitycompleted=0.0000,
            jmppartforecastyearid=0,
            jmppartforecastperiodid=0,
            jmpcreatedby='ppadmin',
            jmpjobpriorityid=0,
            jmpscheduledstarthour=0.00,
            jmpscheduledduehour=0.00,
            jmpshiporganizationid=new_sales_order.ompcustomerorganizationid,
        )

        Salesorderjoblinks.objects.create(
            omjsalesorderid=new_sales_order_line.omlsalesorderid,
            omjsalesorderlineid=new_sales_order_line.omlsalesorderlineid,
            omjsalesorderjoblinkid=1,
            omjlinktype=1,
            omjsalesorderdeliveryid=1,
            omjjobid=job_id,
            omjclosed=False,
            omjcreatedby='ppadmin'
        )

        Jobassemblies.objects.create(
            jmajobid=job_id,
            jmajobassemblyid=0,
            jmalevel=1,
            jmaparentassemblyid=0,
            jmapartid=new_sales_order_line.omlpartid,
            jmapartrevisionid=new_sales_order_line.omlpartrevisionid,
            jmapartwarehouselocationid='MAIN',  # TODO Hardcode Alert
            jmapartbinid='NONE',  # TODO Hardcode Alert
            jmaunitofmeasure='EA',  # TODO Hardcode Alert
            jmapartshortdescription=new_sales_order_line.omlpartshortdescription,
            jmapartlongdescriptionrtf=new_sales_order_line.omlpartlongdescriptionrtf,
            jmapartlongdescriptiontext=new_sales_order_line.omlpartlongdescriptiontext,
            jmaquantityperparent=1.00000,
            jmaestimatedunitcost=0.0000,
            jmaorderquantity=item.root_component.deliver_quantity,
            jmainventoryquantity=0.0000,
            jmascrapquantity=job.jmpscrapquantity,
            jmareworkquantity=0.0000,
            jmaquantitytoinspect=0.0000,
            jmaquantitytoreturn=0.0000,
            jmascheduledstarthour=0.00,
            jmaquantityreceivedtoinventory=0.0000,
            jmareceivedcomplete=False,
            jmascheduledduehour=0.00,
            jmaproductionquantity=0.0000,
            jmaquantitytomake=item.root_component.make_quantity,
            jmaquantitytopull=0.0000,
            jmaquantityissued=0.0000,
            jmapullallfromstock=False,
            jmaissuedcomplete=False,
            jmaoverlapsourceoperationid=0,
            jmaassemblyoverlap=0,
            jmaoverlapsourcelink=0,
            jmaoverlapdestinationlink=0,
            jmaoverlapoffsettime=0.00,
            jmaoverlapoperationid=0,
            jmaoverlaptype=0,
            jmaproductioncomplete=False,
            jmaquantitycompleted=0.0000,
            jmaclosed=False,
            jmascrapquantitycompleted=0.0000,
            jmacreatedby='ppadmin'
        )

        pdx = 10

        for op in item.root_component.shop_operations:
            workcenter_code_cv = op.get_variable(self._exporter.erp_config.workcenter_code_op_variable_name)
            workcenter: Workcenters = None
            if workcenter_code_cv:
                workcenters: [Workcenters] = Workcenters.objects.filter(xawworkcenterid=workcenter_code_cv)
                if len(workcenters) > 0:
                    workcenter = workcenters[0]
            process_code_cv = op.get_variable(self._exporter.erp_config.process_type_op_variable_name)
            process: Processes = None
            if process_code_cv:
                processes: [Processes] = Processes.objects.filter(xacprocessid=process_code_cv)
                if len(processes) > 0:
                    process = processes[0]

            quantityperassembly = 1
            Joboperations.objects.create(
                jmojobid=job.jmpjobid,
                jmojobassemblyid=0,
                jmojoboperationid=pdx,
                jmooperationtype=1,
                jmoaddedoperation=False,
                jmoprototypeoperation=False,
                jmoworkcenterid=workcenter.xawworkcenterid if workcenter else 'INSP',
                jmoprocessid=process.xacprocessid if process else 'INSP',
                jmoprocessshortdescription=process.xacshortdescription if process else 'INSPECTION',
                jmoprocesslongdescriptionrtf=process.xaclongdescriptionrtf if process else 'Inspect and Ship',
                jmoprocesslongdescriptiontext=process.xaclongdescriptiontext if process else 'Inspect and Ship',
                jmoquantityperassembly=quantityperassembly,
                jmoqueuetime=0.00,
                jmosetuphours=op.setup_time if op.setup_time is not None else 0.00,
                jmoproductionstandard=op.runtime if op.runtime is not None else 0.00,
                jmostandardfactor='HP',
                jmosetuprate=0.00,
                jmoproductionrate=0.00,
                jmooverheadrate=27.00,
                jmooperationquantity=quantityperassembly * item.root_component.make_quantity,
                jmoquantitycomplete=0.0000,
                jmosetuppercentcomplete=0,
                jmoactualsetuphours=0.00,
                jmoactualproductionhours=0.00,
                jmoquantitytoinspect=0.00,
                jmoscrapquantityreceived=0.00,
                jmoquantitytoreturn=0.00,
                jmomovetime=0.00,
                jmosetupcomplete=False,
                jmoproductioncomplete=False,
                jmooverlapsourcelink=0,
                jmooverlapdestinationlink=0,
                jmooverlap=0,
                jmooverlapoperationid=0,
                jmooverlapoffsettime=0,
                jmomachinetype=1,
                jmoworkcentermachineid=0,
                jmopartid=job.jmppartid,
                jmopartrevisionid=job.jmppartrevisionid,
                jmopartwarehouselocationid='MAIN',  # TODO Hardcode Alert
                jmopartbinid='NONE',  # TODO Hardcode Alert
                jmounitofmeasure='EA',  # TODO Hardcode Alert
                jmofirm=False,
                jmoestimatedunitcost=0.0000,
                jmominimumcharge=0.00,
                jmosetupcharge=0.00,
                jmocalculatedunitcost=0.00,
                jmoquantitybreak1=0.0000,
                jmounitcost1=0.0000,
                jmoquantitybreak2=0.0000,
                jmounitcost2=0.0000,
                jmoquantitybreak3=0.0000,
                jmounitcost3=0.0000,
                jmoquantitybreak4=0.0000,
                jmounitcost4=0.0000,
                jmoquantitybreak5=0.0000,
                jmounitcost5=0.0000,
                jmoquantitybreak6=0.0000,
                jmounitcost6=0.0000,
                jmoquantitybreak7=0.0000,
                jmounitcost7=0.0000,
                jmoquantitybreak8=0.0000,
                jmounitcost8=0.0000,
                jmoquantitybreak9=0.0000,
                jmounitcost9=0.0000,
                jmoestimatedproductionhours=0.00,
                jmocompletedsetuphours=0.00,
                jmocompletedproductionhours=0.00,
                jmosfemessagertf=op.notes,
                jmosfemessagetext=op.notes,
                jmoclosed=False,
                jmoinspectioncomplete=False,
                jmoinspectionstatus=0,
                jmoinspectiontype=0,
                jmomachinestoschedule=1,
                jmocreatedby='ppadmin',
                jmostarthour=0.00,
                jmoduehour=0.00,
            )
            pdx += 10
        last_index = self.create_component_job_materials(job_id=job_id, children=item.components)
        self.create_material_job_materials(job_id=job_id,
                                           material_operations=item.root_component.material_operations,
                                           start_index=last_index,
                                           material_type_op_variable_name=self._exporter.erp_config.material_type_op_variable_name)

    @staticmethod
    def create_component_job_materials(job_id: str, children: [OrderComponent], start_index: int = 1) -> int:
        cdx = start_index
        for child in children:
            if child.is_root_component:
                continue
            part, rev = PartUtils.get_create_component_part(component=child)
            unit_cost = ProcessJobs.get_component_unit_cost(component=child)
            Jobmaterials.objects.create(
                jmmjobid=job_id,
                jmmjobassemblyid=0,
                jmmjobmaterialid=cdx,
                jmmpartid=part.imppartid,
                jmmpartrevisionid=rev.imrpartrevisionid,
                jmmpartwarehouselocationid='MAIN',  # TODO Hardcode Alert
                jmmpartbinid='NONE',  # TODO Hardcode Alert
                jmmunitofmeasure='EA',  # TODO Hardcode Alert
                jmmpartshortdescription=part.impshortdescription,
                jmmpartlongdescriptionrtf=part.implongdescriptionrtf,
                jmmpartlongdescriptiontext=part.implongdescriptiontext,
                jmmquantityperassembly=1,
                jmmscrappercent=0.00,
                jmmscrapquantity=0.0000,
                jmmestimatedquantity=1,
                jmmestimatedunitcost=unit_cost,
                jmmminimumcharge=0.0000,
                jmmcalculatedunitcost=unit_cost,
                jmmkitpart=False,
                jmmquantitybreak1=0.0000,
                jmmunitcost1=0.0000,
                jmmquantitybreak2=0.0000,
                jmmunitcost2=0.0000,
                jmmquantitybreak3=0.0000,
                jmmunitcost3=0.0000,
                jmmquantitybreak4=0.0000,
                jmmunitcost4=0.0000,
                jmmquantitybreak5=0.0000,
                jmmunitcost5=0.0000,
                jmmquantitybreak6=0.0000,
                jmmunitcost6=0.0000,
                jmmquantitybreak7=0.0000,
                jmmunitcost7=0.0000,
                jmmquantitybreak8=0.0000,
                jmmunitcost8=0.0000,
                jmmquantitybreak9=0.0000,
                jmmunitcost9=0.0000,
                jmmfirm=False,
                jmmleadtime=0,
                jmmquantityallocated=0.0000,
                jmmquantitytoreturn=0.0000,
                jmmquantityreceived=0.0000,
                jmmscrapquantityreceived=0.0000,
                jmmreceivedcomplete=False,
                jmmrelatedjoboperationid=0,
                jmmbackflush=False,
                jmmclosed=False,
                jmmquantitytoinspect=0.0000,
                jmmleadtime1=0,
                jmmleadtime2=0,
                jmmleadtime3=0,
                jmmleadtime4=0,
                jmmleadtime5=0,
                jmmleadtime6=0,
                jmmleadtime7=0,
                jmmleadtime8=0,
                jmmleadtime9=0,
                jmmcostoverride=False,
                jmmpurchasetojobquantity=0.0000,
                jmmpullfromstockquantity=0.0000,
                jmmpullallfromstock=False,
                jmmcreatedby='ppadmin'
            )
            cdx += 1
        return cdx

    @staticmethod
    def get_component_unit_cost(component: OrderComponent) -> float:
        if component.is_hardware:
            return float(component.purchased_component.piece_price.raw_amount)
        else:
            total_cost = 0.00
            qty = component.deliver_quantity if component.deliver_quantity and component.deliver_quantity != 0 else 1
            for s_op in component.shop_operations:
                total_cost += float(s_op.cost.raw_amount)
            for m_op in component.material_operations:
                total_cost += float(m_op.cost.raw_amount)

            return float(total_cost / qty)

    @staticmethod
    def create_material_job_materials(job_id: str, material_operations: [OrderOperation],
                                      material_type_op_variable_name: str = '', start_index: int = 1,) -> int:
        mdx = start_index
        for mop in material_operations:
            type_name = mop.get_variable(material_type_op_variable_name)
            if not type_name:
                continue
            part, rev = PartUtils.get_create_placeholder_parts(part_number=type_name, short_description='',
                                                               long_description='')
            Jobmaterials.objects.create(
                jmmjobid=job_id,
                jmmjobassemblyid=0,
                jmmjobmaterialid=mdx,
                jmmpartid=part.imppartid,
                jmmpartrevisionid=rev.imrpartrevisionid,
                jmmpartwarehouselocationid='MAIN',  # TODO Hardcode Alert
                jmmpartbinid='NONE',  # TODO Hardcode Alert
                jmmunitofmeasure='EA',  # TODO Hardcode Alert
                jmmpartshortdescription=type_name,
                jmmpartlongdescriptionrtf=mop.name,
                jmmpartlongdescriptiontext=mop.name,
                jmmquantityperassembly=1,
                jmmscrappercent=0.00,
                jmmscrapquantity=0.0000,
                jmmestimatedquantity=1,
                jmmestimatedunitcost=mop.cost.raw_amount,
                jmmminimumcharge=0.0000,
                jmmcalculatedunitcost=mop.cost.raw_amount,
                jmmkitpart=False,
                jmmquantitybreak1=0.0000,
                jmmunitcost1=0.0000,
                jmmquantitybreak2=0.0000,
                jmmunitcost2=0.0000,
                jmmquantitybreak3=0.0000,
                jmmunitcost3=0.0000,
                jmmquantitybreak4=0.0000,
                jmmunitcost4=0.0000,
                jmmquantitybreak5=0.0000,
                jmmunitcost5=0.0000,
                jmmquantitybreak6=0.0000,
                jmmunitcost6=0.0000,
                jmmquantitybreak7=0.0000,
                jmmunitcost7=0.0000,
                jmmquantitybreak8=0.0000,
                jmmunitcost8=0.0000,
                jmmquantitybreak9=0.0000,
                jmmunitcost9=0.0000,
                jmmfirm=False,
                jmmleadtime=0,
                jmmquantityallocated=0.0000,
                jmmquantitytoreturn=0.0000,
                jmmquantityreceived=0.0000,
                jmmscrapquantityreceived=0.0000,
                jmmreceivedcomplete=False,
                jmmrelatedjoboperationid=0,
                jmmbackflush=False,
                jmmclosed=False,
                jmmquantitytoinspect=0.0000,
                jmmleadtime1=0,
                jmmleadtime2=0,
                jmmleadtime3=0,
                jmmleadtime4=0,
                jmmleadtime5=0,
                jmmleadtime6=0,
                jmmleadtime7=0,
                jmmleadtime8=0,
                jmmleadtime9=0,
                jmmcostoverride=False,
                jmmpurchasetojobquantity=0.0000,
                jmmpullfromstockquantity=0.0000,
                jmmpullallfromstock=False,
                jmmcreatedby='ppadmin'
            )
            mdx += 1
        return mdx
