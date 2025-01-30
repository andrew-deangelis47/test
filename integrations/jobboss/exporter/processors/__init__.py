from baseintegration.exporter.processor import BaseProcessor
from typing import Union


class JobBossProcessor(BaseProcessor):
    """
    This is the default processor for all JobBoss processor classes.
    Class methods variables are used to track state based on subsequent processor class methods that inherit this class.
    """

    # set this flag to T/F on whether a rollback should happen.
    do_rollback = False
    suffix = ""
    facing = 0
    jb_calculator_qty = 0
    jb_configured_unit_cost = 0
    rounded = True
    parent_component = None
    pp_operation_to_jb_work_center_mapping: Union[dict, None] = None
