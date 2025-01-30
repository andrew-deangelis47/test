import json
import unittest
from unittest.mock import patch

from plex.objects.routing import Operation, PartOperation
from plex.client import PlexClient
import os


class TestOperations(unittest.TestCase):
    def setup(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), "data/operation.json"), 'r') as f:
            self.mock_op = json.load(f)

        PlexClient()  # Initialize the singleton
        self.maxDiff = 650

    def test_get(self):
        self.setup()
        with patch.object(PlexClient, 'get_resource', return_value=self.mock_op) as mock_get_resource:
            op = Operation.get(1)

            mock_get_resource.assert_called_once_with(Operation.get_resource_name('get'), 1)

            mock_op = self.mock_op

            assert op.id == mock_op['id']
            assert op.code == mock_op['code']
            assert op.type == mock_op['type']
            assert op.inventoryType == mock_op['inventoryType']


class TestPartOperations(unittest.TestCase):
    def setup(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), "data/part_operation.json"), 'r') as f:
            self.mock_op = json.load(f)

        PlexClient()  # Initialize the singleton
        self.maxDiff = 650

    def test_get(self):
        self.setup()
        with patch.object(PlexClient, 'get_resource', return_value=self.mock_op) as mock_get_resource:
            op = PartOperation.get(1)

            mock_get_resource.assert_called_once_with(PartOperation.get_resource_name('get'), 1)

            mock_op = self.mock_op

            assert op.id == mock_op['id']
            assert op.type == mock_op['type']
            assert op.partId == mock_op['partId']
            assert op.operationId == mock_op['operationId']
            assert op.operationNumber == mock_op['operationNumber']
            assert op.active == mock_op['active']
            assert op.subOperation == mock_op['subOperation']
            assert op.shippable == mock_op['shippable']
            assert op.multiple == mock_op['multiple']
            assert op.netWeight == mock_op['netWeight']
