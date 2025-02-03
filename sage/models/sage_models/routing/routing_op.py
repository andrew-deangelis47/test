from sage.models.sage_models import BaseObject


class RoutingOp(BaseObject):
    SEQUENCE = [
        ('entity_type', 0),
        ('operation', 1),
        ('alternate_index', 2),
        ('start_date', 3),
        ('end_date', 4),
        ('standard_op', 5),
        ('main_work_center', 6),
        ('labor_work_center', 7),
        ('labor_time_set_fac', 8),
        ('labor_r_time_fact', 9),
        ('ope_description', 10),
        ('operation_uom', 11),
        ('stk_ope_converstion', 12),
        ('number_of_resources', 13),
        ('number_labor_res', 14),
        ('percent_efficiency', 15),
        ('shrinkage_in_percentage', 16),
        ('run_time_code', 16),
        ('management_unit', 17),
        ('base_quantity', 18),
        ('preparation_time', 19),
        ('setup_time', 20),
        ('run_time', 21),
        ('rate', 22),
        ('waiting_time', 23),
        ('post_run_time', 24),
        ('subcontract', 25),
        ('subcontract_prod', 26),
        ('operation_text_1', 27),
        ('operation_text_2', 28),
        ('operation_text_3', 29),
    ]

    # 30 elements in the L section
    TOTAL_ELEMENTS = 30

    entity_type: str
    operation: str
    alternate_index: str
    start_date: str
    end_date: str
    standard_op: str
    main_work_center: str
    labor_work_center: str
    labor_time_set_fac: str
    labor_r_time_fact: str
    ope_description: str
    operation_uom: str
    stk_ope_converstion: str
    number_of_resources: str
    number_labor_res: str
    percent_efficiency: str
    shrinkage_in_percentage: str
    run_time_code: str
    management_unit: str
    base_quantity: str
    preparation_time: str
    setup_time: str
    run_time: str
    rate: str
    waiting_time: str
    post_run_time: str
    subcontract: str
    subcontract_prod: str
    operation_text_1: str
    operation_text_2: str
    operation_text_3: str

    def __init__(self):
        self.entity_type: str = 'L'
        self.operation: str = '10'
        self.alternate_index: str = ''
        self.start_date: str = ''
        self.end_date: str = ''
        self.standard_op: str = '10'
        self.main_work_center: str = 'MTRLS'
        self.labor_work_center: str = ''
        self.labor_time_set_fac: str = ''
        self.labor_r_time_fact: str = ''
        self.ope_description: str = 'Material Dispatch'
        self.operation_uom: str = 'EA'
        self.stk_ope_converstion: str = ''
        self.number_of_resources: str = '1'
        self.number_labor_res: str = ''
        self.percent_efficiency: str = '100.000'
        self.shrinkage_in_percentage: str = ''
        self.run_time_code: str = 'Proportional'
        self.management_unit: str = 'Time for 1'
        self.base_quantity: str = '1.000'
        self.preparation_time: str = ''
        self.setup_time: str = '0.0160'
        self.run_time: str = ''
        self.rate: str = ''
        self.waiting_time: str = ''
        self.post_run_time: str = ''
        self.subcontract: str = 'No'
        self.subcontract_prod: str = ''
        self.operation_text_1: str = ''
        self.operation_text_2: str = ''
        self.operation_text_3: str = ''
