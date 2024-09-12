import pytest

from src.edge import Edge
from src.panel import Panel
from src.location import RelativeLocation
from src.orientation import Orientation
from src.node import Node, ConnectorNode, CornerNode
from src.object_registry import ObjectRegistry

###############################################################################
# Node Tests
###############################################################################
def test_node_initialization():
    edge = Edge(Panel(Orientation.FLOOR))
    relative_location = RelativeLocation(1, 2, 3)
    node = Node(edge, relative_location)
    assert node.edge == edge
    assert node.relative_location == relative_location
    assert node.mate == None
    assert node == ObjectRegistry.get_object_by_id(node.id)

def test_invalid_params_node_initialisation():
    edge = Edge(Panel(Orientation.FLOOR))
    relative_location = RelativeLocation(1, 2, 3)
    with pytest.raises(TypeError):
        node = Node("edge")
    with pytest.raises(TypeError):
        node = Node(edge, "relative_location")
    with pytest.raises(TypeError):
        node = Node(edge, relative_location, "absolute_location")

###############################################################################
# ConnectorNode Tests
###############################################################################
def test_connector_node_initialization():
    edge = Edge(Panel(Orientation.FLOOR))
    connector_node = ConnectorNode(edge)
    assert connector_node.edge == edge
    assert connector_node.mate == None
    assert edge.connector_nodes == [connector_node]
    connector_node_2 = ConnectorNode(edge)
    assert edge.connector_nodes == [connector_node, connector_node_2]

def test_corner_node_edge_setter():
    edge = Edge(Panel(Orientation.FLOOR))
    connector_node = ConnectorNode(edge)
    connector_node_2 = ConnectorNode(edge)
    edge_2 = Edge(Panel(Orientation.WALL))
    connector_node_3 = ConnectorNode(edge_2)
    assert edge.connector_nodes == [connector_node, connector_node_2]
    assert edge_2.connector_nodes == [connector_node_3]
    connector_node_2.edge = edge_2
    assert edge.connector_nodes == [connector_node]
    assert edge_2.connector_nodes == [connector_node_3, connector_node_2]

def test_connector_nodes_mate_with_method():
    edge = Edge(Panel(Orientation.FLOOR))
    connector_node = ConnectorNode(edge)
    edge_2 = Edge(Panel(Orientation.WALL))
    connector_node_2 = ConnectorNode(edge_2)
    edge_3 = Edge(Panel(Orientation.ROOF))
    connector_node_3 = ConnectorNode(edge_3)
    connector_node_4 = ConnectorNode(edge)
    corner_node = CornerNode(edge_2)
    assert connector_node.mate == None
    assert connector_node_2.mate == None

    connector_node.mate_with(connector_node_3)
    assert connector_node.mate == connector_node_3
    assert connector_node_2.mate == None
    assert connector_node_3.mate == connector_node

    # Nodes must be on different edges to mate.
    with pytest.raises(ValueError):
        connector_node.mate_with(connector_node_4)

    # ConnectorNodes cannot mate with CornerNodes
    with pytest.raises(TypeError):
        connector_node.mate_with(corner_node)

    # ConnectorNode can mate with None
    connector_node.mate_with(connector_node_3)
    assert connector_node.mate == connector_node_3
    connector_node.mate_with(None)
    assert connector_node.mate == None

    # Node cannot mate with itself
    with pytest.raises(ValueError):
        connector_node.mate_with(connector_node)

    # Must validate parameters
    with pytest.raises(TypeError):
        connector_node.mate_with("connector_node")

def test_connector_node_is_complete_method():
    edge = Edge(Panel(Orientation.FLOOR))
    connector_node = ConnectorNode(edge)
    connector_node_3 = ConnectorNode(edge)
    relative_location = RelativeLocation(1, 2, 3)
    edge_2 = Edge(Panel(Orientation.WALL))
    connector_node_2 = ConnectorNode(edge_2)
    edge = Edge(Panel(Orientation.FLOOR))

    # Has edge but no relative location or mate (fails)
    assert connector_node.is_complete() == False

    # Has edge and location but no mate (passes)
    connector_node.relative_location = relative_location
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

###############################################################################
# CornerNode Tests
###############################################################################
def test_corner_node_initialization():
    edge = Edge(Panel(Orientation.FLOOR))
    assert edge.corner_nodes == []
    corner_node = CornerNode(edge)
    assert edge.corner_nodes == [corner_node]
    assert corner_node.edge == edge
    assert corner_node.mate == None
    corner_node_2 = CornerNode(edge)
    assert edge.corner_nodes == [corner_node, corner_node_2]
    with pytest.raises(OverflowError):
        corner_node_3 = CornerNode(edge)

def test_corner_node_edge_setter():
    edge = Edge(Panel(Orientation.FLOOR))
    corner_node = CornerNode(edge)
    corner_node_2 = CornerNode(edge)
    edge_2 = Edge(Panel(Orientation.WALL))
    corner_node_3 = CornerNode(edge_2)
    with pytest.raises(OverflowError):
        corner_node_3.edge = edge
    assert edge.corner_nodes == [corner_node, corner_node_2]
    assert edge_2.corner_nodes == [corner_node_3]
    corner_node_2.edge = edge_2
    assert edge.corner_nodes == [corner_node]
    assert edge_2.corner_nodes == [corner_node_3, corner_node_2]

def test_corner_nodes_mate_with_method():
    edge = Edge(Panel(Orientation.FLOOR))
    corner_node = CornerNode(edge)
    edge_2 = Edge(Panel(Orientation.WALL))
    corner_node_2 = CornerNode(edge_2)
    edge_3 = Edge(Panel(Orientation.ROOF))
    corner_node_3 = CornerNode(edge_3)
    corner_node_4 = CornerNode(edge)
    connector_node = ConnectorNode(edge_3)
    assert corner_node.mate == None
    assert corner_node_2.mate == None

    corner_node.mate_with(corner_node_3)
    assert corner_node.mate == corner_node_3
    assert corner_node_2.mate == None
    assert corner_node_3.mate == corner_node

    # Nodes must be on different edges to mate.
    with pytest.raises(ValueError):
        corner_node.mate_with(corner_node_4)

    # CornerNodes cannot mate with ConnectorNodes
    with pytest.raises(TypeError):
        corner_node.mate_with(connector_node)

    # CornerNode can mate with None
    corner_node.mate_with(corner_node_3)
    assert corner_node.mate == corner_node_3
    corner_node.mate_with(None)
    assert corner_node.mate == None

    # A Node cannot mate with itself
    with pytest.raises(ValueError):
        corner_node.mate_with(corner_node)

    # Must validate parameters
    with pytest.raises(TypeError):
        corner_node.mate_with("corner_node")

def test_corner_node_is_complete_method():
    edge = Edge(Panel(Orientation.FLOOR))
    corner_node = CornerNode(edge)
    corner_node_3 = CornerNode(edge)
    relative_location = RelativeLocation(1, 2, 3)
    edge_2 = Edge(Panel(Orientation.WALL))
    corner_node_2 = CornerNode(edge_2)
    edge = Edge(Panel(Orientation.FLOOR))

    # Has edge but no location or mate (fails)
    assert corner_node.is_complete() == False

    # Has edge and location but no mate (fails)
    corner_node.relative_location = relative_location
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
