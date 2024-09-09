import pytest

from src.edge import Edge
from src.panel import Panel
from src.orientation import Orientation
from src.node import Node, ConnectorNode, CornerNode

###############################################################################
# Node Tests
###############################################################################
def test_node_initialization():
    edge = Edge(Panel(Orientation.FLOOR))
    node = Node(edge)
    assert node.edge == edge

def test_invalid_params_node_initialisation():
    with pytest.raises(TypeError):
        node = Node("edge")

###############################################################################
# ConnectorNode Tests
###############################################################################
def test_connector_node_initialization():
    edge = Edge(Panel(Orientation.FLOOR))
    connector_node = ConnectorNode(edge)
    assert connector_node.edge == edge

def test_invalid_params_connector_node_initialisation():
    with pytest.raises(TypeError):
        connector_node = ConnectorNode("edge")

###############################################################################
# CornerNode Tests
###############################################################################
def test_corner_node_initialization():
    edge = Edge(Panel(Orientation.FLOOR))
    corner_node = CornerNode(edge)
    assert corner_node.edge == edge

def test_invalid_params_corner_node_initialisation():
    with pytest.raises(TypeError):
        corner_node = CornerNode("edge")