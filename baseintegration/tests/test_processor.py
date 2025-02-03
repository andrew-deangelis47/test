import pytest
from baseintegration.exporter.processor import BaseProcessor, ProcessNotImplementedError
from baseintegration.exporter import BaseExporter
from baseintegration.integration import Integration


class UnchangedProcessor(BaseProcessor):
    pass


# This is our mock database. This only works for our very abstract purposes. ERP specific tests should be done.
resource_db = {}


class ERPResource:
    def __init__(self, id):
        self.id = id


class ERPProcessor(BaseProcessor):

    do_rollback = True

    def _process(self, res_id: int):
        # print(f'res_id {res_id}')
        # If resource already exists, grab it:
        resource = resource_db.get(res_id, None)
        print()
        if not resource:
            resource = ERPResource(res_id)
            resource_db[res_id] = resource
        return resource

    def _rollback(self, obj, *args):
        # # Find the object int he database and remove:
        # print(f'rollback! obj: {obj} args: {args} kwargs: {kwargs}')
        if resource_db.get(obj.id, None):
            resource_db.pop(obj.id)


class SkipRollbackProcessor(ERPProcessor):
    do_rollback = False


class InheritedProcessor(ERPProcessor):

    def _process(self, param2, identifier=1):
        return super()._process(identifier)


class TestProcessor:

    def test_missing_processor(self):
        # The base processor shouldn't be able to process:
        # try:
        #     BaseProcessor()._process("test")
        # except Exception as pnie:
        #     print(f'exception! {pnie.__class__}, {ProcessNotImplementedError}')
        #     self.assertIsInstance(pnie,ProcessNotImplementedError)
        #     # self.assertIsNotNone(pnie)
        # NOTE: we have to import this from the exporter.processor import, not directly from baseexporter.exporter.exception
        exporter = BaseExporter(Integration())
        with pytest.raises(ProcessNotImplementedError):
            BaseProcessor(exporter)._process("test")
        with pytest.raises(ProcessNotImplementedError):
            UnchangedProcessor(exporter)._process("test")

    def test_has_processor(self):
        # This should run without throwing an error
        # erp_resource = RunnableProcessor._process()
        exporter = BaseExporter(Integration())
        assert isinstance(ERPProcessor(exporter)._process(3), ERPResource)
