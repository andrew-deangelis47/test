from typing import NamedTuple
from paperless.objects.orders import OrderOperation, OrderComponent
from baseintegration.datamigration import logger
import os
import yaml
from django.db import connection


# this has to be in __init__.py because it needs to be defined before the e2 model import
def get_version_number() -> str:
    if os.environ.get('ERP_VERSION'):
        if "syteline_10" in os.environ.get('ERP_VERSION'):
            return "syteline_10"
        else:
            return "default"
    else:
        try:
            with open(os.path.join(os.path.dirname(__file__), "../../config.yaml")) as file:
                # The FullLoader parameter handles the conversion from YAML
                # scalar values to Python the dictionary format
                config_yaml = yaml.load(file, Loader=yaml.FullLoader)
                if config_yaml.get("Paperless") and config_yaml["Paperless"].get("erp_version") and "syteline_10" in \
                        config_yaml["Paperless"]["erp_version"]:
                    return "syteline_10"
        except Exception:
            pass
    return "default"


class ItemData(NamedTuple):
    item_number: str
    component: OrderComponent
    item_is_new: bool
    routing_operations: list


class MaterialData(NamedTuple):
    part_data: ItemData
    material_op: OrderOperation


class ItemProcessorData(NamedTuple):
    manufactured_components: list
    purchased_components: list
    materials: list


def get_part_number_and_name(component):
    # Could be either a component or operation - based on whether we're creating a component or material item
    if isinstance(component, OrderOperation):
        logger.info("Getting part number out of material")
        part_number = component.get_variable("Item")
        part_name = part_number
    else:
        part_number = component.part_number
        if not part_number:
            part_number = str(component.part_name)[0:30]
        part_name = component.part_name
    logger.info(f"Processing part with part number {part_number}")
    return part_number, part_name


def add_notes(object_name, row_pointer, note_desc, note_text, database_name, internal_flag=1):
    note_text = note_text.replace("'", '') if note_text else None
    with open(os.path.join(os.path.dirname(__file__), "../../config.yaml")) as file:
        config_yaml = yaml.load(file, Loader=yaml.FullLoader)
        if 'op_internal_flag' in config_yaml["Exporters"]["orders"]:
            internal_flag = config_yaml["Exporters"]["orders"].get("op_internal_flag")
    with connection.cursor() as cursor:
        sql = f"""USE [{database_name}];
            SET NOCOUNT ON;
            DECLARE	@Infobar InfobarType;
            EXEC [dbo].[CreateSpecificNoteSp]
            @ObjectName = '{object_name}',
            @RowPointer = '{row_pointer}',
            @NoteDesc = '{note_desc}',
            @NoteText = '{note_text}',
            @InternalFlag = {internal_flag},
            @Infobar = @Infobar OUTPUT"""
        logger.info(f"SQL being run is {sql}")
        cursor.execute(sql)
