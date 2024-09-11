import pytest

from src.panel import Panel
from src.orientation import Orientation
from src.edge import Edge
from src.location import RelativeLocation, AbsoluteLocation
from src.node import ConnectorNode, CornerNode

# Test initialization
def test_edge_initialization():
    panel = Panel(Orientation.FLOOR)
    edge = Edge(panel)
    assert edge.panel == panel

def test_invalid_params_edge_initialisation():
    with pytest.raises(TypeError):
        edge = Edge("panel")

###############################################################################
# Test methods
###############################################################################
# Panel methods
def test_edge_panel_getter_and_setter():
    panel = Panel(Orientation.FLOOR)
    panel_2 = Panel(Orientation.ROOF)
    edge = Edge(panel)
    assert edge.panel == panel
    assert panel.edges == [edge]
    edge.panel = panel_2
    assert panel.edges == []
    assert panel_2.edges == [edge]
    assert edge.panel == panel_2
    with pytest.raises(TypeError):
        edge.panel = "panel"
    

def test_edge_panel_setter_with_invalid_parameters():
    panel = Panel(Orientation.FLOOR)
    panel_2 = "Panel"
    edge = Edge(panel)
    with pytest.raises(TypeError): 
        edge.panel = panel_2

# ConnectorNodes methods
def test_edge_connector_nodes_getter_and_setter():
    panel = Panel(Orientation.FLOOR)
    edge = Edge(panel)
    assert edge.connector_nodes == []
    connector_node = ConnectorNode(edge)
    edge.connector_nodes = [connector_node]
    assert edge.connector_nodes == [connector_node]

def test_edge_connector_nodes_setter_with_invalid_parameters():
    panel = Panel(Orientation.FLOOR)
    edge = Edge(panel)
    connector_node = "ConnectorNode"
    with pytest.raises(TypeError):
        edge.connector_nodes = connector_node
    with pytest.raises(TypeError):
        edge.connector_nodes = [connector_node]
    with pytest.raises(TypeError):
        edge.connector_nodes = [ConnectorNode(edge), connector_node]

def test_edge_add_connector_nodes():
    panel = Panel(Orientation.FLOOR)
    edge = Edge(panel)
    connector_node = ConnectorNode(edge)
    # I am breaking encapsulation to test add_connector_nodes which occurs
    # automatically upon ConnectorNode creation.
    edge._connector_nodes = []
    assert edge.connector_nodes == []
    edge.add_connector_nodes([connector_node])
    assert edge.connector_nodes == [connector_node]
    connector_node_2 = ConnectorNode(edge)
    connector_node_3 = ConnectorNode(edge)
    connector_node_4 = ConnectorNode(edge)
    # I am breaking encapsulation to test add_connector_nodes which occurs
    # automatically upon ConnectorNode creation.
    edge._connector_nodes = []
    assert edge.connector_nodes == []
    edge.add_connector_nodes([connector_node_2, connector_node_3])
    assert edge.connector_nodes == [connector_node_2,
                                    connector_node_3]
    edge.add_connector_nodes(connector_node_4)
    assert edge.connector_nodes == [connector_node_2,
                                    connector_node_3,
                                    connector_node_4]

def test_edge_add_connector_nodes_with_invalid_parameters():
    panel = Panel(Orientation.FLOOR)
    edge = Edge(panel)
    with pytest.raises(TypeError):
        edge.add_connector_nodes("ConnectorNode")
    with pytest.raises(TypeError):
        edge.add_connector_nodes(["ConnectorNode"])
    with pytest.raises(TypeError):
        edge.add_connector_nodes([ConnectorNode(edge),"ConnectorNode"])

# CornerNodes Methods
def test_edge_corner_nodes_getter_and_setter():
    panel = Panel(Orientation.FLOOR)
    edge = Edge(panel)
    assert edge.corner_nodes == []
    corner_node = CornerNode(edge)
    edge.corner_nodes = [corner_node]
    assert edge.corner_nodes == [corner_node]

def test_edge_corner_nodes_setter_with_invalid_parameters():
    panel = Panel(Orientation.FLOOR)
    edge = Edge(panel)
    edge_2 = Edge(panel)
    corner_node_string = "CornerNode"
    corner_node = CornerNode(edge)
    corner_node_2 = CornerNode(edge)
    with pytest.raises(TypeError):
        edge.corner_nodes = corner_node_string
    with pytest.raises(TypeError):
        edge.corner_nodes = [corner_node_string]
    with pytest.raises(TypeError):
        edge.corner_nodes = [corner_node, corner_node_string]
    # An edge is not allowed to have the two corners nodes be the same instance
    with pytest.raises(ValueError):
        edge.corner_nodes = [corner_node, corner_node]
    # An edge cannot have three or more corner nodes
    with pytest.raises(ValueError):
        edge.corner_nodes = [corner_node, corner_node_2, corner_node]
    with pytest.raises(OverflowError):
        corner_node_3 = CornerNode(edge)
    with pytest.raises(OverflowError):
        corner_node_3 = CornerNode(edge_2)
        corner_node_3.edge = edge

# is_complete Method
def test_edge_is_complete():
    panel_0 = Panel(Orientation.ROOF)
    edge = Edge(panel_0)
    edge_2 = Edge(panel_0)
    corner_node = CornerNode(edge, RelativeLocation(0, 0, 0))
    corner_node_2 = CornerNode(edge, RelativeLocation(1, 0, 0))
    corner_node_3 = CornerNode(edge_2)
    corner_node_4 = CornerNode(edge_2)
    connector_node = ConnectorNode(edge, RelativeLocation(0.5, 0, 0))
    connector_node_2 = ConnectorNode(edge_2, RelativeLocation(0, 0, 0))

    edge.connector_nodes = [connector_node]
    corner_node.mate_with(corner_node_3)
    corner_node_2.mate_with(corner_node_4)
    edge.corner_nodes = [corner_node, corner_node_2]
    assert edge.is_complete()

    # Edge needs to belong to a panel
    with pytest.raises(TypeError):
        edge = Edge()

    # Needs to have two and only two CornerNodes
    edge.corner_nodes = []
    assert not edge.is_complete()
    edge.corner_nodes = [corner_node]
    assert not edge.is_complete()
    with pytest.raises(ValueError):
        edge.corner_nodes = [corner_node, corner_node_2, corner_node]
    edge.corner_nodes = [corner_node, corner_node_2]
    assert edge.is_complete()

    # The CornerNodes need to have different locations
    corner_node_2.relative_location = RelativeLocation(0, 0, 0)
    assert not edge.is_complete()
    corner_node_2.relative_location = RelativeLocation(1, 0, 0)
    assert edge.is_complete()

    # There needs to be at least one ConnectorNode
    edge.connector_nodes = []
    assert not edge.is_complete()
    edge.connector_nodes = [connector_node]
    assert edge.is_complete()


    # All nodes in _corner_nodes and _connector_nodes need to point to this
    # edge instance.
    edge.corner_nodes = [corner_node, corner_node_3]
    assert not edge.is_complete()
    edge.corner_nodes = [corner_node, corner_node_2]
    assert edge.is_complete()
    edge.connector_nodes = [connector_node, connector_node_2]
    assert not edge.is_complete()
    edge.connector_nodes = [connector_node]
    assert edge.is_complete()

    # The location of all nodes in _connector_nodes need to lie on the 
    # geometric line between the two nodes in _corner_nodes.
    connector_node.relative_location = RelativeLocation(-1, 0, 0)
    assert not edge.is_complete()
    connector_node.relative_location = RelativeLocation(0, 1, 0)
    assert not edge.is_complete()
    connector_node.relative_location = RelativeLocation(1, 1, 1)
    assert not edge.is_complete()
    connector_node.relative_location = RelativeLocation(0.5, 0, 0)
    assert edge.is_complete()

    # All nodes that point to this edge instance need to be either in 
    # _corner_nodes or _connector_nodes
    connector_node_5 = ConnectorNode(edge, RelativeLocation(1, 2, 3))
    assert not edge.is_complete()
    # Delete connector_node_5 once the destroy method has been written for Node