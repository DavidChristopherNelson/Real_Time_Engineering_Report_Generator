import pytest
import uuid

from src.panel import Panel
from src.orientation import Orientation
from src.edge import Edge
from src.node import Node, ConnectorNode, CornerNode
from src.object_registry import ObjectRegistry

# Objects are added to the registry automatically upon instantiation
def test_add_object_and_get_object_by_id():
    panel = Panel(Orientation.FLOOR)
    assert ObjectRegistry.get_object_by_id(panel.id) == panel
    edge = Edge(panel)
    assert ObjectRegistry.get_object_by_id(edge.id) == edge
    node = Node(edge)
    assert ObjectRegistry.get_object_by_id(node.id) == node
    connector_node = ConnectorNode(edge)
    assert ObjectRegistry.get_object_by_id(connector_node.id) == connector_node
    corner_node = CornerNode(edge)
    assert ObjectRegistry.get_object_by_id(corner_node.id) == corner_node

def test_remove_object():
    panel = Panel(Orientation.FLOOR)
    assert ObjectRegistry.get_object_by_id(panel.id) == panel
    ObjectRegistry.remove_object_by_id(panel.id)
    assert ObjectRegistry.get_object_by_id(panel.id) == None

def test_size():
    size = ObjectRegistry.size()
    panel = Panel(Orientation.FLOOR)
    assert ObjectRegistry.size() == size + 1
    ObjectRegistry.remove_object_by_id(panel.id)
    assert ObjectRegistry.size() == size

def test_is_unique():
    new_id = uuid.uuid4()
    assert ObjectRegistry.is_unique(new_id) == True
    panel = Panel(Orientation.FLOOR)
    assert ObjectRegistry.is_unique(panel.id) == False

def test_generate_id():
    new_id = ObjectRegistry.generate_id()
    assert isinstance(new_id, uuid.UUID)
    assert ObjectRegistry.is_unique(new_id) == True