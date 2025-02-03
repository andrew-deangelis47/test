from dynamics.client_factory import DynamicsConfig
from baseintegration.utils.operations import OperationUtils


class DynamicsBaseFactory:

    config: DynamicsConfig
    op_utils: OperationUtils

    def __init__(self, config: DynamicsConfig, op_utils: OperationUtils):
        self.config = config
        self.op_utils = op_utils
