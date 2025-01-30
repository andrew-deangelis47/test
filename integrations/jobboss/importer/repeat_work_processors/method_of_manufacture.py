from baseintegration.importer.import_processor import BaseImportProcessor
import jobboss.models as jb
from baseintegration.utils.repeat_work_objects import MethodOfManufacture, Part, Header
from jobboss.utils.repeat_work_utils import RepeatPartUtilObject, QuoteMOMUtil, JobMOMUtil, \
    QuantityNode, get_quote_erp_code
from baseintegration.utils import safe_get, logger
from typing import List


class MethodOfManufactureProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util_object: RepeatPartUtilObject):
        logger.info("MethodOfManufactureProcessor - Attempting to create MethodOfManufacture")
        self.source_database = self._importer.source_database

        repeat_part = repeat_part_util_object.repeat_part
        if repeat_part is None:
            return None

        repeat_part.methods_of_manufacture = []

        self.create_methods_of_manufacture_from_jb_quote(repeat_part_util_object)
        self.create_methods_of_manufacture_from_jb_job(repeat_part_util_object)
        self.create_methods_of_manufacture_from_jb_quote_hardware(repeat_part_util_object)
        self.create_methods_of_manufacture_from_jb_job_hardware(repeat_part_util_object)
        return repeat_part_util_object

    def create_methods_of_manufacture_from_jb_quote(self, repeat_part_util_object: RepeatPartUtilObject):
        for jb_quote in repeat_part_util_object.jb_quotes_queryset:
            logger.info(f"Creating MethodOfManufacture from JobBOSS Quote: {jb_quote.rfq}")

            # Get quantity breaks for each line item in the list
            jb_quoted_qtys = jb.QuoteQty.objects.using(self.source_database).filter(quote=jb_quote.quote).order_by('quote_qty')

            # Create a new MOM for each quantity break
            for position, jb_qty in enumerate(jb_quoted_qtys, start=0):

                # Recursively get parents and then multiply out the "true" assembly tree quantities for each qty break
                logger.info("Attempting to recursively get the true assembly quantity.")
                self.node_quantities = []
                requested_qty = self.get_assembly_adjusted_quantity(jb_quote, jb_qty, position)

                quote_method_of_manufacture = MethodOfManufacture(
                    make_qty=int(jb_qty.make_quantity),
                    requested_qty=requested_qty,
                    unit_price=float(jb_qty.unit_price),
                    total_price=float(safe_get(jb_qty, "total_price", 0))
                )

                quote_mom_util = QuoteMOMUtil(jb_quote, jb_qty, quote_method_of_manufacture)
                repeat_part_util_object.quote_mom_utils.append(quote_mom_util)

    def get_assembly_adjusted_quantity(self, jb_quote: jb.Quote, jb_qty: jb.QuoteQty, position):
        if jb_quote.assembly_level == 0:
            # If nodes exist, this is an assembly.
            if len(self.node_quantities) > 0:
                root_node = self.node_quantities[-1]
                true_quantity = root_node.parent_qty * root_node.qty_per_parent  # Root parent_qty * qty_per_parent
                # Remove the last node because it is the root (already accounted for above)
                self.node_quantities = self.node_quantities[:-1]

                # Reverse the order so that qtys are multiplied out in depth order from the root comp. downward
                for node in self.node_quantities[::-1]:
                    true_quantity = node.qty_per_parent * true_quantity

                return true_quantity
            # If there are no nodes. This must be a root component. Return the actual quantity.
            else:
                return int(jb_qty.quote_qty)
        else:
            # Get parent quote from bill of quotes relationship
            jb_node = jb.BillOfQuotes.objects.using(self.source_database).filter(component_quote=jb_quote).first()
            if not jb_node:
                logger.info(
                    f"Could not find BillOfQuotes object for quote id: {jb_quote.quote}.\n"
                    f"Assigning 'quote_qty' from jb.QuoteQty object which may be incorrect due to yield."
                )
                return int(jb_qty.quote_qty)

            jb_parent_quote = jb_node.parent_quote

            # Get quantities associated with the parent
            parent_qtys = jb.QuoteQty.objects.using(self.source_database).filter(quote=jb_parent_quote.quote).order_by('quote_qty')

            # Use the index position to determine which quantity we actually care about (they're ordered)
            correct_qty_break_qty = [qty.quote_qty for qty in parent_qtys][position]

            # Assign the correct qty to the dictionary that will be used to multiply out the quantities
            new_node = QuantityNode(jb_node.relationship_qty, correct_qty_break_qty)
            self.node_quantities.append(new_node)

            # Recursively call the function until you get to the root
            true_quantity = self.get_assembly_adjusted_quantity(jb_parent_quote, jb_qty, position)
        return true_quantity

    def create_methods_of_manufacture_from_jb_job(self, repeat_part_util_object: RepeatPartUtilObject):
        for jb_job in repeat_part_util_object.jb_jobs_queryset:
            logger.info(f"Creating MethodOfManufacture from JobBOSS Job: {jb_job.job}")

            # Create a new MOM for the single job quantity on each job
            job_method_of_manufacture = MethodOfManufacture(
                make_qty=int(jb_job.order_quantity),
                requested_qty=int(jb_job.make_quantity),
                total_price=float(safe_get(jb_job, "total_price", 0)),
                unit_price=float(jb_job.unit_price),
            )

            job_mom_util = JobMOMUtil(jb_job, job_method_of_manufacture)
            repeat_part_util_object.job_mom_utils.append(job_mom_util)

    def create_methods_of_manufacture_from_jb_quote_hardware(self, repeat_part_util_object: RepeatPartUtilObject):
        for jb_quote_req in repeat_part_util_object.jb_quote_hardware_queryset:
            try:
                jb_quote = jb_quote_req.quote
                logger.info(f"Creating MethodOfManufacture from JobBOSS QuoteReq (hardware) for Quote: {jb_quote.quote}")
            except Exception as e:
                logger.info(f"Orphan part. Skipping. {e}")
                continue

            quote_erp_code = get_quote_erp_code(jb_quote)

            # Get quantity breaks for each line item in the list
            jb_quoted_qtys = jb.QuoteReqQty.objects.using(self.source_database).filter(quote_req=jb_quote_req.quote_req).order_by('est_qty')

            # Get whichever quantity line we're looking at and set it to the position index
            # Once you have the position index, get the QuoteQty object for this specific hardware comp.
            # Pass the QuoteQty object into the adjusted_assembly() func. to get the normalized qty of the parent comp.
            # Multiply the hardware qty_per by the normalized parent qty.

            # Create a new MOM for each quantity break
            for position, jb_qty in enumerate(jb_quoted_qtys, start=0):
                jb_quote_qty = self.get_quote_qty_object_for_parent_quote(jb_quote, position)

                # Recursively get parents and then multiply out the "true" assembly tree quantities for each qty break
                logger.info("Attempting to recursively get the true assembly quantity.")
                self.node_quantities = []
                true_parent_quantity = self.get_assembly_adjusted_quantity(jb_quote, jb_quote_qty, position)

                quote_method_of_manufacture = MethodOfManufacture(
                    make_qty=int(jb_qty.make_quantity),
                    requested_qty=int(jb_quote_req.quantity_per) * true_parent_quantity,
                    unit_price=jb_qty.est_unit_cost,  # TODO: Validate that these are the right prices
                    children=[],
                )

                quote_method_of_manufacture.operations = []  # Hardware materials can't have operations
                quote_method_of_manufacture.required_materials = []  # Hardware materials can't have materials

                # There is no subsequent processing for hardware. Append each MOM to the repeat part.
                repeat_part: Part = repeat_part_util_object.repeat_part
                headers: List[Header] = repeat_part.headers
                for header in headers:
                    if header.erp_code == quote_erp_code:
                        header.methods_of_manufacture.append(quote_method_of_manufacture.to_json())

    def get_quote_qty_object_for_parent_quote(self, jb_quote: jb.Quote, position: int) -> jb.QuoteQty:
        # There should be an equal amount of quote qtys for hardware qtys, ordered by qty
        # The first position QuoteReqQty should correspond with the first position QuoteQty object
        # Get the quote qty object for this hardware qty break
        jb_quote_qtys = jb.QuoteQty.objects.filter(quote=jb_quote.quote).order_by('quote_qty')
        return jb_quote_qtys[position]

    def create_methods_of_manufacture_from_jb_job_hardware(self, repeat_part_util_object: RepeatPartUtilObject):
        for jb_material_req in repeat_part_util_object.jb_job_hardware_queryset:
            try:
                jb_job = jb_material_req.job
                logger.info(f"Creating MethodOfManufacture from JobBOSS MaterialReq (hardware) for Job: {jb_job.job}")
            except Exception as e:
                logger.info(f"Orphan part. Skipping. {e}")
                continue

            job_method_of_manufacture = MethodOfManufacture(
                make_qty=int(jb_job.order_quantity),
                requested_qty=int(jb_material_req.est_qty),
                unit_price=jb_material_req.est_unit_cost,
                children=[],
            )

            job_method_of_manufacture.operations = []  # Hardware materials can't have operations
            job_method_of_manufacture.required_materials = []  # Hardware materials can't have materials

            # There is no subsequent processing for hardware. Append each MOM to the repeat part.
            repeat_part: Part = repeat_part_util_object.repeat_part
            headers: List[Header] = repeat_part.headers
            for header in headers:
                if header.erp_code == jb_job.top_lvl_job:
                    header.methods_of_manufacture.append(job_method_of_manufacture.to_json())
