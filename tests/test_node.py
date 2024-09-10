import pytest

from src.edge import Edge
from src.panel import Panel
from src.location import Location
from src.orientation import Orientation
from src.node import Node, ConnectorNode, CornerNode

###############################################################################
# Node Tests
###############################################################################
def test_node_initialization():
    edge = Edge(Panel(Orientation.FLOOR))
    location = Location(1, 2, 3)
    node = Node(edge, location)
    assert node.edge == edge
    assert node.location == location
    assert node.mate == None

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
    connector_node_4 = ConnectorNode(edge)
    assert connector_node.mate == None
    assert connector_node_2.mate == None

    connector_node.mate_with(connector_node_3)
    assert connector_node.mate == connector_node_3
    assert connector_node_2.mate == None
    assert connector_node_3.mate == connector_node

    # Nodes must be on different edges to mate.
    with pytest.raises(ValueError):
        connector_node.mate_with(connector_node_4)

def test_connector_node_is_complete_method():
    edge = Edge(Panel(Orientation.FLOOR))
    connector_node = ConnectorNode(edge)
    connector_node_3 = ConnectorNode(edge)
    location = Location(1, 2, 3)
    edge_2 = Edge(Panel(Orientation.WALL))
    connector_node_2 = ConnectorNode(edge_2)
    edge = Edge(Panel(Orientation.FLOOR))

    # Has edge but no location or mate (fails)
    assert connector_node.is_complete() == False

    # Has edge and location but no mate (passes)
    connector_node.location = location
    assert connector_node.is_complete() == True

    # Has edge and location and a legitimate mate (passes)
    connector_node.mate_with(connector_node_2)
    assert connector_node.is_complete() == True

    # Has edge and location but mate is illegitimate (shares same edge) (fails)
    with pytest.raises(ValueError):
        connector_node.mate_with(connector_node_3)

    # Has edge and location but mate is illegitimate (mates with itself)(fails)
    with pytest.raises(ValueError):
        connector_node.mate_with(connector_node)
    
    # Has edge and a legitimate mate but no location.
    connector_node_4 = ConnectorNode(edge_2)
    connector_node_4.mate_with(connector_node)
    print("starting failed assertion")
    assert connector_node_4.is_complete() == False

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
    corner_node_4 = CornerNode(edge)
    assert corner_node.mate == None
    assert corner_node_2.mate == None

    corner_node.mate_with(corner_node_3)
    assert corner_node.mate == corner_node_3
    assert corner_node_2.mate == None
    assert corner_node_3.mate == corner_node

    # Nodes must be on different edges to mate.
    with pytest.raises(ValueError):
        corner_node.mate_with(corner_node_4)

def test_corner_node_is_complete_method():
    edge = Edge(Panel(Orientation.FLOOR))
    corner_node = CornerNode(edge)
    corner_node_3 = CornerNode(edge)
    location = Location(1, 2, 3)
    edge_2 = Edge(Panel(Orientation.WALL))
    corner_node_2 = CornerNode(edge_2)
    edge = Edge(Panel(Orientation.FLOOR))

    # Has edge but no location or mate (fails)
    assert corner_node.is_complete() == False

    # Has edge and location but no mate (fails)
    corner_node.location = location
    assert corner_node.is_complete() == False

    # Has edge and location and a legitimate mate (passes)
    corner_node.mate_with(corner_node_2)
    assert corner_node.is_complete() == True

    # Has edge and location but mate is illegitimate (shares same edge) (fails)
    with pytest.raises(ValueError):
        corner_node.mate_with(corner_node_3)

    # Has edge and location but mate is illegitimate (mates with itself)(fails)
    with pytest.raises(ValueError):
        corner_node.mate_with(corner_node)
    
    # Has edge and a legitimate mate but no location.
    corner_node_4 = CornerNode(edge_2)
    corner_node_4.mate_with(corner_node)
    print("starting failed assertion")
    assert corner_node_4.is_complete() == False
