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
    assert connector_node.mate == None

def test_invalid_params_connector_node_initialisation():
    with pytest.raises(TypeError):
        connector_node = ConnectorNode("edge")

def test_connector_nodes_mate_with_method():
    edge = Edge(Panel(Orientation.FLOOR))
    connector_node = ConnectorNode(edge)
    edge_2 = Edge(Panel(Orientation.WALL))
    connector_node_2 = ConnectorNode(edge_2)
    edge_3 = Edge(Panel(Orientation.ROOF))
    connector_node_3 = ConnectorNode(edge_3)
    assert connector_node.mate == None
    assert connector_node_2.mate == None

    connector_node.mate_with(connector_node_3)
    assert connector_node.mate == connector_node_3
    assert connector_node_2.mate == None
    assert connector_node_3.mate == connector_node

###############################################################################
# CornerNode Tests
###############################################################################
def test_corner_node_initialization():
    edge = Edge(Panel(Orientation.FLOOR))
    corner_node = CornerNode(edge)
    assert corner_node.edge == edge
    assert corner_node.mate == None

def test_invalid_params_corner_node_initialisation():
    with pytest.raises(TypeError):
        corner_node = CornerNode("edge")

def test_corner_nodes_mate_with_method():
    edge = Edge(Panel(Orientation.FLOOR))
    corner_node = CornerNode(edge)
    edge_2 = Edge(Panel(Orientation.WALL))
    corner_node_2 = CornerNode(edge_2)
    edge_3 = Edge(Panel(Orientation.ROOF))
    corner_node_3 = CornerNode(edge_3)
    assert corner_node.mate == None
    assert corner_node_2.mate == None

    corner_node.mate_with(corner_node_3)
    assert corner_node.mate == corner_node_3
    assert corner_node_2.mate == None
    assert corner_node_3.mate == corner_node