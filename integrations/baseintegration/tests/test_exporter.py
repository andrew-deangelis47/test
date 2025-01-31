import pytest
from ...baseintegration.exporter.exceptions import IntegrationNotImplementedError
from ...baseintegration.exporter.order_exporter import OrderExporter
from ...baseintegration.exporter.quote_exporter import QuoteExporter
from ...baseintegration.exporter import ProcessorNotRegisteredError, BaseExporter
from paperless.objects.orders import Order
from paperless.objects.quotes import Quote
from ...baseintegration.utils.test_utils import get_quote, get_order
from test_processor import ERPResource, ERPProcessor, resource_db
from ...baseintegration.integration import Integration
from ...baseintegration.datamigration import logger
import requests_mock


class UnchangedOrderExporter(OrderExporter):
    pass


class UnchangedQuoteExporter(QuoteExporter):
    pass


class RunnableOrderExporter(OrderExporter):
    def _process_order(self, order: Order):
        # shouldn't throw an error
        logger.info(f"Running {order.number}")
        return 0


class RunnableQuoteExporter(QuoteExporter):
    def _process_quote(self, quote: Quote):
        return 0


@pytest.fixture
def setup_order():
    # load client
    Integration()
    return get_order(1)


@pytest.fixture
def setup_quote():
    # load client
    Integration()
    return get_quote(1)


class TestIntegration:

    def test_missing_process_order(self, setup_order):
        # The base integrations shouldn't work if _process_order isn't overridden
        with pytest.raises(IntegrationNotImplementedError):
            OrderExporter(Integration())._process_order(setup_order)
        with pytest.raises(IntegrationNotImplementedError):
            UnchangedOrderExporter(Integration())._process_order(setup_order)

    def test_missing_process_quote(self, setup_quote):
        # The base integrations shouldn't work if _process_order isn't overridden
        with pytest.raises(IntegrationNotImplementedError):
            QuoteExporter(Integration())._process_quote(setup_quote)
        with pytest.raises(IntegrationNotImplementedError):
            UnchangedQuoteExporter(Integration())._process_quote(setup_quote)

    def test_process_order(self, setup_order):
        ri = RunnableOrderExporter(Integration())
        assert isinstance(ri, RunnableOrderExporter)
        ri._process_order(setup_order)

    def test_process_quote(self, setup_quote):
        ri = RunnableQuoteExporter(Integration())
        assert isinstance(ri, RunnableQuoteExporter)
        ri._process_quote(setup_quote)

    def test_cannot_run_base_exporter(self):
        base_exporter = BaseExporter(Integration())
        with pytest.raises(IntegrationNotImplementedError):
            base_exporter.run()

        class Test:

            pass

        assert base_exporter.get_processor_instance(Test) is None

    def test_integration_run_order(self, setup_order, caplog):
        ri = RunnableOrderExporter(Integration())
        ri.run(order_num=1)
        assert "Running single order" in caplog.text

    def test_integration_run_quote(self, setup_quote, caplog):
        ri = RunnableQuoteExporter(Integration())
        ri.run(quote_num="1")
        assert "Running single quote" in caplog.text

    def test_integration_run_order_listener(self, caplog):
        int1 = Integration()
        ri = RunnableOrderExporter(int1)
        int_id = int1.managed_integration_uuid
        with requests_mock.Mocker(real_http=True) as mock:
            mock.get(f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/poll",
                     text="""{
                                "has_more_events": false,
                                "results": [
                                    {
                                        "created": "2022-06-21T19:32:30.143624Z",
                                        "data": {
                                            "uuid": "f0dcfcb6-c22b-4b0c-8a14-f8cc8e2f2738",
                                            "number": 1
                                        },
                                        "related_object_type": "supplier order",
                                        "related_object": "f0dcfcb6-c22b-4b0c-8a14-f8cc8e2f2738",
                                        "type": "order.created",
                                        "uuid": "fd6d85d4-4167-4cc1-9ab1-10705c256e52"
                                    }
                                ]
                            }""",
                     status_code=200)
            mock.get(
                f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/integration_actions/abc-123",
                text='{"type": '
                     '"export_order",'
                     '"uuid": '
                     '"abc-123",'
                     '"updated": "2021-11-30T17:09:39.052737Z",'
                     '"created": "2021-11-30T17:08:41.811913Z",'
                     '"status": "queued",'
                     '"status_message": '
                     'null,"entity_id": '
                     '"1"}',
                status_code=200)
            mock.patch(
                f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/integration_actions/abc-123",
                text='{"type": '
                     '"export_order",'
                     '"uuid": '
                     '"abc-123",'
                     '"status": "in_progress",'
                     '"status_message": '
                     'null,"entity_id": '
                     '"1","current_record_count": "0"}',
                status_code=200)
            mock.post(
                f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}",
                text='{"type": '
                     '"export_order",'
                     '"uuid": '
                     '"abc-123",'
                     '"status": "in_progress",'
                     '"status_message": '
                     'null,"entity_id": '
                     '"1" , "current_record_count": "0"}',
                status_code=200
            )
            ri.run()
        assert "Running order listener" in caplog.text
        assert "1 new orders were found to export" in caplog.text

    def test_integration_order_sort(self, caplog):
        int1 = Integration()
        ri = RunnableOrderExporter(int1)
        int_id = int1.managed_integration_uuid
        with requests_mock.Mocker(real_http=True) as mock:
            mock.get(f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/poll",
                     text="""{
                                            "has_more_events": false,
                                            "results": [
                                                {
                                                    "created": "2022-06-23T19:32:30.143624Z",
                                                    "data": {
                                                        "uuid": "f0dcfcb6-c22b-4b0c-8a14-f8cc8e2f2738",
                                                        "number": 2
                                                    },
                                                    "related_object_type": "supplier order",
                                                    "related_object": "f0dcfcb6-c22b-4b0c-8a14-f8cc8e2f2738",
                                                    "type": "order.created",
                                                    "uuid": "fd6d85d4-4167-4cc1-9ab1-10705c256e52"
                                                },
                                                {
                                                    "created": "2022-06-21T19:32:30.143624Z",
                                                    "data": {
                                                        "uuid": "f0dcfcb6-c22b-4b0c-8a14-f8cc8e2f2738",
                                                        "number": 1
                                                    },
                                                    "related_object_type": "supplier order",
                                                    "related_object": "f0dcfcb6-c22b-4b0c-8a14-f8cc8e2f2738",
                                                    "type": "order.created",
                                                    "uuid": "fd6d85d4-4167-4cc1-9ab1-10705c256e52"
                                                }
                                            ]
                                        }""",
                     status_code=200)
            mock.get(
                f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/integration_actions/abc-123",
                text='{"type": '
                     '"export_order",'
                     '"updated": "2021-11-30T17:19:39.052737Z",'
                     '"created": "2021-11-30T17:08:41.811913Z",'
                     '"uuid": '
                     '"abc-123",'
                     '"status": "queued",'
                     '"status_message": '
                     'null,"entity_id": '
                     '"2"}',
                status_code=200)
            mock.get(
                f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/integration_actions/cde-123",
                text='{"type": '
                     '"export_order",'
                     '"updated": "2021-11-30T17:19:39.052737Z",'
                     '"created": "2021-11-30T17:08:41.811913Z",'
                     '"uuid": '
                     '"cde-123",'
                     '"status": "queued",'
                     '"status_message": '
                     'null,"entity_id": '
                     '"1"}',
                status_code=200)
            mock.patch(
                f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/integration_actions/abc-123",
                text='{"type": '
                     '"export_order",'
                     '"uuid": '
                     '"abc-123",'
                     '"status": "in_progress",'
                     '"status_message": '
                     'null,"entity_id": '
                     '"2"}',
                status_code=200)
            mock.patch(
                f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/integration_actions/cde-123",
                text='{"type": '
                     '"export_order",'
                     '"uuid": '
                     '"cde-123",'
                     '"status": "in_progress",'
                     '"status_message": '
                     'null,"entity_id": '
                     '"1"}',
                status_code=200)
            mock.post(
                f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}",
                text='{"type": '
                     '"export_order",'
                     '"uuid": '
                     '"abc-123",'
                     '"status": "in_progress",'
                     '"status_message": '
                     'null,"entity_id": '
                     '"1"}',
                status_code=200
            )

            ri.run()
            assert "Running order listener" in caplog.text
            assert "2 new orders were found to export" in caplog.text
            index = caplog.text.find("Running 1")
            second_index = caplog.text.find("Running 2")
            assert index < second_index

    def test_integration_run_quote_listener(self, caplog):
        int1 = Integration()
        ri = RunnableQuoteExporter(int1)
        int_id = int1.managed_integration_uuid
        with requests_mock.Mocker(real_http=True) as mock:
            mock.get(f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/poll",
                     text="""{
                                            "has_more_events": false,
                                            "results": [
                                                {
                                                    "created": "2022-06-21T19:32:30.143624Z",
                                                    "data": {
                                                        "uuid": "f0dcfcb6-c22b-4b0c-8a14-f8cc8e2f2738",
                                                        "number": 100,
                                                        "revision_number": null
                                                    },
                                                    "related_object_type": "quote",
                                                    "related_object": "f0dcfcb6-c22b-4b0c-8a14-f8cc8e2f2738",
                                                    "type": "quote.sent",
                                                    "uuid": "fd6d85d4-4167-4cc1-9ab1-10705c256e52"
                                                }
                                            ]
                                        }""",
                     status_code=200)
            mock.get(
                f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/integration_actions/abc-123",
                text='{"type": '
                     '"export_quote",'
                     '"uuid": '
                     '"abc-123",'
                     '"updated": "2021-11-30T17:09:39.052737Z",'
                     '"created": "2021-11-30T17:08:41.811913Z",'
                     '"status": "queued",'
                     '"status_message": '
                     'null,"entity_id": '
                     '"100"}',
                status_code=200)
            mock.patch(
                f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/integration_actions/abc-123",
                text='{"type": '
                     '"export_quote",'
                     '"uuid": '
                     '"abc-123",'
                     '"status": "in_progress",'
                     '"status_message": '
                     'null,"entity_id": '
                     '"100"}',
                status_code=200)
            mock.post(
                f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}",
                text='{"type": '
                     '"export_order",'
                     '"uuid": '
                     '"abc-123",'
                     '"status": "in_progress",'
                     '"status_message": '
                     'null,"entity_id": '
                     '"1"}')
            ri.run()
        assert "Running quote listener" in caplog.text
        assert "1 new quotes were found to export" in caplog.text

    def test_integration_send_email(self, caplog):
        ri = RunnableOrderExporter(Integration())
        ri.send_email("test", "test")
        assert "No destination emails found. Not sending email" in caplog.text

    def test_process_resource(self):
        # can we get a resource back?
        ri = RunnableOrderExporter(Integration())
        ri.register_processor(ERPResource, ERPProcessor)

        with ri.process_resource(ERPResource, 1) as resource:
            assert isinstance(resource, ERPResource)
            assert resource.id == 1
            # The resource should be in the DB right now:
            db_val = resource_db.get(1, None)
            assert db_val == resource
            assert db_val.id == resource.id
            with ri.process_resource(ERPResource, 2) as resource2:
                assert isinstance(resource2, ERPResource)
                assert resource2.id == 2
                # The resource should be in the DB right now:
                db_val2 = resource_db.get(2, None)
                assert db_val2 == resource2
                assert db_val2.id == resource2.id

    def test_remove_processor(self):
        ri = RunnableOrderExporter(Integration())
        ri.register_processor(ERPResource, ERPProcessor)
        ri.remove_processor(ERPResource)
        with pytest.raises(ProcessorNotRegisteredError):
            with ri.process_resource(ERPResource, 1):
                pass

    def test_send_email(self, caplog):
        ri = RunnableOrderExporter(Integration())
        ri.send_email("test", "test")
        assert "No destination emails found. Not sending email" in caplog.text

    """
    def test_get_resource_rollback(self):
        # can we get a resource back?
        ri = RunnableIntegration()
        ri.register_processor(ERPResource, ERPProcessor)

        with ri.process_resource(ERPResource, 1) as resource:
            assert isinstance(resource, ERPResource)
            assert resource.id == 1
            # The resource should be in the DB right now:
            db_val = resource_db.get(1, None)
            assert db_val == resource
            assert db_val.id == resource.id
            with ri.process_resource(ERPResource, 2) as resource2:
                assert isinstance(resource2, ERPResource)
                assert resource2.id == 2
                # The resource should be in the DB right now:
                db_val2 = resource_db.get(2, None)
                assert db_val2 == resource2
                assert db_val2.id == resource2.id
        assert resource_db.get(1, None) is None
        assert resource_db.get(2, None) is None
    """
