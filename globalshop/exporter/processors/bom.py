from typing import Dict, List

from paperless.objects.components import AssemblyComponent

from globalshop.client import GlobalShopClient
from paperless.objects.orders import OrderItem

from globalshop.exporter.processors import GSProcessor
from globalshop.bom import BOM
from globalshop.utils import pad_part_num


class BOMProcessor(GSProcessor):

    def _process(self, item: OrderItem):
        if item.root_component.type == 'assembled':
            # For each purchased component in the assembly, add a BOM line
            # for child in root_component.children:
            root_component = item.root_component
            if root_component.part_number is not None:
                partnumber = root_component.part_number
            else:
                partnumber = root_component.part_name
            top_bom_part_number = pad_part_num(partnumber)
            top_bom_rev_number = root_component.revision

            parents_by_child_id: Dict[int, List[AssemblyComponent]] = {}
            for component in item.iterate_assembly():
                for child_id in component.component.child_ids:
                    parents_by_child_id.setdefault(child_id, [])
                    parents_by_child_id[child_id].append(component)

            for component in item.iterate_assembly():
                # TODO: Make this a param, b/c some may want to add all components
                #  to BOM
                # if component.component.is_hardware:
                # sequence += 1
                bom_complete = False
                if component.component.is_root_component:
                    bom_complete = True
                if root_component.part_number is not None:
                    comp_partnumber = component.component.part_number
                else:
                    comp_partnumber = component.component.part_name

                component_part_number = pad_part_num(comp_partnumber)
                component_rev_number = component.component.revision

                comments = ''
                description = component.component.description
                source = self.get_source(component.component)

                if component.parent:
                    for parent in parents_by_child_id.get(component.component.id, []):
                        if parent.component.part_number is not None:
                            parent_partnumber = parent.component.part_number
                        else:
                            parent_partnumber = parent.component.part_name
                        parent_part_number = pad_part_num(parent_partnumber)
                        parent_rev_number = parent.component.revision
                        level = parent.level + 1
                        qty = component.component.innate_quantity
                        for child in parent.component.children:
                            if child.child_id == component.component.id:
                                qty = child.quantity

                        BOM.insert(external_id=top_bom_part_number,
                                   top_bom=top_bom_part_number,
                                   top_bom_rev=top_bom_rev_number,
                                   parent_part=parent_part_number,
                                   parent_rev=parent_rev_number,
                                   part_number=component_part_number,
                                   part_number_rev=component_rev_number,
                                   level=level,
                                   quantity=qty,
                                   description=description,
                                   source=source,
                                   comments=comments,
                                   bom_complete=bom_complete)
                else:
                    # If this is a flat bom, we still want to add them as linked
                    # to the top level BOM
                    parent_rev_number = top_bom_rev_number
                    parent_part_number = top_bom_part_number
                    level = component.level
                    qty = component.component.innate_quantity

                    BOM.insert(external_id=top_bom_part_number,
                               top_bom=top_bom_part_number,
                               top_bom_rev=top_bom_rev_number,
                               parent_part=parent_part_number,
                               parent_rev=parent_rev_number,
                               part_number=component_part_number,
                               part_number_rev=component_rev_number,
                               level=level,
                               quantity=qty,
                               description=description,
                               source=source,
                               comments=comments,
                               bom_complete=bom_complete)

            # We have cached all the SQL INSERT statements by calling the
            # BOM.insert. We now need to execute the cache:
            client: GlobalShopClient = GlobalShopClient.get_instance()
            client.execute_cache(commit=True)

    def get_source(self, component) -> str:
        """
        Source for FG/FC is Manuf to Job, PP - Purchased to Job
        values are one character: J, P, G, F
        """
        if component.is_root_component:
            # source = 'Manuf to Job'
            source = 'F'
        elif component.is_hardware:
            # source = 'Purch to Job'
            source = 'J'
        elif component.process and component.process.external_name == 'Customer Furnished':
            # source = 'Consign to Job'
            source = 'G'
        else:
            # source = 'Manuf to Job'
            source = 'F'
        return source
