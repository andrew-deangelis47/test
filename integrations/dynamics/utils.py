from baseintegration.datamigration import BaseDataMigration
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.exporter import BaseProcessor
from paperless.objects.quotes import QuoteOperation, QuoteComponent


def get_quantity(component: QuoteComponent):
    """
    Returns the default quantity for a component.
    """
    quantities = component.quantities
    if quantities:
        return quantities[0].quantity
    else:
        return 1


class DynamicsOpVariableMixin:
    """
    This is an abstract class to be subclassed by classes whose objects have a single associated ERP config.
    It provides various utilities regarding the retrieval of operation variable values.
    """
    def get_config(self):
        """
        This should be overridden to return the ERP config to reference.
        """
        raise NotImplementedError

    def get_config_value(self, config_key: str):
        """
        Returns the value of the given ERP config setting.
        """
        return getattr(self.get_config(), config_key)

    def get_operation_variable(self, operation: QuoteOperation, config_key: str):
        """
        Returns the value of the operation variable specified by the given ERP config key.
        """
        var_name = self.get_config_value(config_key)
        return operation.get_variable(var_name)

    def get_operation_variable_for_quantity(self, operation: QuoteOperation, config_key: str, quantity: int,
                                            return_row=False):
        """
        Returns the value of the quantity-specific operation variable specified by the given ERP config key.
        """
        var_name = self.get_config_value(config_key)
        var_val = operation.get_variable_for_qty(var_name, quantity)
        if var_val and var_val.value is not None:
            return var_val.row if return_row else var_val.value

    def get_quantity_operation_variable(self, operation: QuoteOperation, config_key: str, component: QuoteComponent,
                                        return_row=False):
        """
        Returns the value of the quantity-specific operation variable specified by the given ERP config key, with
        the quantity determined by the default quantity of the given component.
        """
        return self.get_operation_variable_for_quantity(operation, config_key, get_quantity(component), return_row)

    def get_op_var_values(self, component: QuoteComponent, config_key: str, return_row=False):
        """
        Returns all values of the quantity-specific operation variable specified by the given ERP config key, searching
        over all shop operations on the component, with the quantity determined by the default quantity of the given
        component.
        """
        results = []
        for operation in component.shop_operations:
            val = self.get_quantity_operation_variable(operation, config_key, component, return_row)
            if val is not None:
                results.append(val)
        return results


class DynamicsDataMigration(BaseDataMigration, DynamicsOpVariableMixin):
    def get_config(self):
        return self.erp_config


class DynamicsExportProcessor(BaseProcessor, DynamicsOpVariableMixin):
    def get_config(self):
        return self._exporter.erp_config


class DynamicsImportProcessor(BaseImportProcessor, DynamicsOpVariableMixin):
    def get_config(self):
        return self._importer.erp_config
