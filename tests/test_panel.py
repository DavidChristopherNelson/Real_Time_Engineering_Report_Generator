import pytest

from src.panel import Panel
from src.orientation import Orientation
from src.location import AbsoluteLocation, RelativeLocation
from src.edge import Edge
from src.node import ConnectorNode, CornerNode

# Panel Initialisation Tests
def test_panel_orientation_initialization():
    floor_orientation = Orientation.FLOOR
    panel = Panel(floor_orientation)
    assert panel.orientation == floor_orientation
    wall_orientation = Orientation.WALL
    panel = Panel(wall_orientation)
    assert panel.orientation == wall_orientation
    roof_orientation = Orientation.ROOF
    panel = Panel(roof_orientation)
    assert panel.orientation == roof_orientation

def test_panel_default_location_initialization():
    panel = Panel(Orientation.FLOOR)
    assert panel.absolute_location.x == None
    assert panel.absolute_location.y == None
    assert panel.absolute_location.z == None

def test_panel_location_initialization():
    panel = Panel(Orientation.FLOOR, AbsoluteLocation(1, 2, 3))
    assert panel.absolute_location.x == 1
    assert panel.absolute_location.y == 2
    assert panel.absolute_location.z == 3

def test_invalid_params_panel_initialisation():
    with pytest.raises(TypeError):
        panel = Panel("floor")
    with pytest.raises(TypeError):
        fake_absolute_location = [1, 2, 3]
        panel = Panel(Orientation.FLOOR, fake_absolute_location)

# Panel Method Tests
def test_edges_setter_and_getter():
    panel = Panel(Orientation.FLOOR, AbsoluteLocation(1, 2, 3))
    edge_1 = Edge(panel)
    edge_2 = Edge(panel)
    edge_3 = Edge(panel)
    edge_4 = Edge(panel)
    panel.edges = [edge_1, edge_2, edge_3, edge_4]
    assert panel.edges[0] == edge_1
    assert panel.edges[1] == edge_2
    assert panel.edges[2] == edge_3
    assert panel.edges[3] == edge_4

def test_panel_is_complete():
    panel = Panel(Orientation.FLOOR, AbsoluteLocation(0, 0, 0))
    edge_1 = Edge(panel)
    edge_2 = Edge(panel)
    edge_3 = Edge(panel)
    edge_4 = Edge(panel)
    panel.edges = [edge_1, edge_2, edge_3, edge_4]
    edge_1_corner_1 = CornerNode(edge_1, RelativeLocation(0, 0, 0))
    edge_1_corner_2 = CornerNode(edge_1, RelativeLocation(1, 0, 0))
    edge_1_connector = ConnectorNode(edge_1, RelativeLocation(0.5, 0, 0))
    edge_1.corner_nodes = [edge_1_corner_1, edge_1_corner_2]
    edge_1.connector_nodes = [edge_1_connector]
    edge_2_corner_1 = CornerNode(edge_2, RelativeLocation(1, 0, 0))
    edge_2_corner_2 = CornerNode(edge_2, RelativeLocation(1, 1, 0))
    edge_2_connector = ConnectorNode(edge_2, RelativeLocation(1, 0.5, 0))
    edge_2.corner_nodes = [edge_2_corner_1, edge_2_corner_2]
    edge_2.connector_nodes = [edge_2_connector]
    edge_3_corner_1 = CornerNode(edge_3, RelativeLocation(1, 1, 0))
    edge_3_corner_2 = CornerNode(edge_3, RelativeLocation(0, 1, 0))
    edge_3_connector = ConnectorNode(edge_3, RelativeLocation(0.5, 1, 0))
    edge_3.corner_nodes = [edge_3_corner_1, edge_3_corner_2]
    edge_3.connector_nodes = [edge_3_connector]
    edge_4_corner_1 = CornerNode(edge_4, RelativeLocation(0, 1, 0))
    edge_4_corner_2 = CornerNode(edge_4, RelativeLocation(0, 0, 0))
    edge_4_connector = ConnectorNode(edge_4, RelativeLocation(0, 0.5, 0))
    edge_4.corner_nodes = [edge_4_corner_1, edge_4_corner_2]
    edge_4.connector_nodes = [edge_4_connector]

    edge_1_corner_1.mate_with(edge_4_corner_2)
    edge_2_corner_1.mate_with(edge_1_corner_2)
    edge_3_corner_1.mate_with(edge_2_corner_2)
    edge_4_corner_1.mate_with(edge_3_corner_2)

    assert edge_1.is_complete()
    assert edge_2.is_complete()
    assert edge_3.is_complete()
    assert edge_4.is_complete()
    assert panel.is_complete()

    # Panel needs to have an orientation to be complete
    with pytest.raises(TypeError):
        panel("orientation", AbsoluteLocation(1, 1, 1))

    # Panel needs to have an location to be complete
    with pytest.raises(TypeError):
        panel.absolute_location = "Location"

    # Panel needs to have exactly four edges to be complete
    assert panel.is_complete()
    panel.edges = [edge_1, edge_2, edge_3]
    assert not panel.is_complete()
    panel.edges = [edge_1, edge_2, edge_3, edge_4, Edge(panel)]
    assert not panel.is_complete()
    panel.edges = [edge_1, edge_2, edge_3, edge_4]
    assert panel.is_complete()    

    # All of the panel's edges need to be complete
    edge_1.connector_nodes = []
    assert not panel.is_complete()
    edge_1.connector_nodes = [edge_1_connector]
    assert panel.is_complete()
    # Test other ways that edges can be incomplete

    # The corners of the edges cannot mate with corners from edges
    # belonging to other panels.
    panel_2 = Panel(Orientation.FLOOR, AbsoluteLocation(1, 1, 1))
    edge_5 = Edge(panel_2)
    edge_5_corner_1 = CornerNode(edge_5, RelativeLocation(0, 0, 0))
    edge_5_corner_2 = CornerNode(edge_5, RelativeLocation(10, 0, 0))
    edge_5_connector = ConnectorNode(edge_5, RelativeLocation(0.5, 0, 0))
    edge_5.corner_nodes = [edge_5_corner_1, edge_5_corner_2]
    edge_5.connector_nodes = [edge_5_connector]
    edge_6 = Edge(panel_2)
    edge_6_corner_1 = CornerNode(edge_6, RelativeLocation(0, 0, 0))
    edge_6_corner_2 = CornerNode(edge_6, RelativeLocation(20, 0, 0))
    edge_6_connector = ConnectorNode(edge_6, RelativeLocation(0.5, 0, 0))
    edge_6.corner_nodes = [edge_6_corner_1, edge_6_corner_2]
    edge_6.connector_nodes = [edge_6_connector]
    assert panel.is_complete()

    edge_1_corner_1.mate_with(edge_5_corner_1)
    edge_4_corner_2.mate_with(edge_6_corner_1)
    assert not panel.is_complete()
    edge_1_corner_1.mate_with(edge_4_corner_2)
    assert panel.is_complete()

    # The two corner nodes in each edge cannot mate with corner nodes from
    # the same edge
    # Break all the mates.
    edge_1_corner_1.mate_with(None)
    edge_2_corner_1.mate_with(None)
    edge_3_corner_1.mate_with(None)
    edge_4_corner_1.mate_with(None)
    
    # Move the lines so that the new mates can satisfy mate co-locatility
    # (which hasn't been enforced at the time of writing)
    edge_2_corner_1.relative_location = RelativeLocation(0, 0, 0)
    edge_2_corner_2.relative_location = RelativeLocation(1, 0, 0)
    edge_4_corner_1.relative_location = RelativeLocation(1, 1, 0)
    edge_4_corner_2.relative_location = RelativeLocation(0, 1, 0)

    # Make sure that the edges don't just pair up but form enclosed rectangles. 
    b_panel = Panel(Orientation.FLOOR, AbsoluteLocation(0, 0, 0))
    b_edge_1 = Edge(b_panel)
    b_edge_2 = Edge(b_panel)
    b_edge_3 = Edge(b_panel)
    b_edge_4 = Edge(b_panel)
    b_panel.edges = [b_edge_1, b_edge_2, b_edge_3, b_edge_4]
    b_edge_1_corner_1 = CornerNode(b_edge_1, RelativeLocation(0, 0, 0))
    b_edge_1_corner_2 = CornerNode(b_edge_1, RelativeLocation(1, 0, 0))
    b_edge_1_connector = ConnectorNode(b_edge_1, RelativeLocation(0.5, 0, 0))
    b_edge_1.corner_nodes = [b_edge_1_corner_1, b_edge_1_corner_2]
    b_edge_1.connector_nodes = [b_edge_1_connector]
    b_edge_2_corner_1 = CornerNode(b_edge_2, RelativeLocation(0, 0, 0))
    b_edge_2_corner_2 = CornerNode(b_edge_2, RelativeLocation(1, 0, 0))
    b_edge_2_connector = ConnectorNode(b_edge_2, RelativeLocation(0.5, 0, 0))
    b_edge_2.corner_nodes = [b_edge_2_corner_1, b_edge_2_corner_2]
    b_edge_2.connector_nodes = [b_edge_2_connector]
    b_edge_3_corner_1 = CornerNode(b_edge_3, RelativeLocation(1, 1, 0))
    b_edge_3_corner_2 = CornerNode(b_edge_3, RelativeLocation(0, 1, 0))
    b_edge_3_connector = ConnectorNode(b_edge_3, RelativeLocation(0.5, 1, 0))
    b_edge_3.corner_nodes = [b_edge_3_corner_1, b_edge_3_corner_2]
    b_edge_3.connector_nodes = [b_edge_3_connector]
    b_edge_4_corner_1 = CornerNode(b_edge_4, RelativeLocation(1, 1, 0))
    b_edge_4_corner_2 = CornerNode(b_edge_4, RelativeLocation(0, 1, 0))
    b_edge_4_connector = ConnectorNode(b_edge_4, RelativeLocation(0.5, 1, 0))
    b_edge_4.corner_nodes = [b_edge_4_corner_1, b_edge_4_corner_2]
    b_edge_4.connector_nodes = [b_edge_4_connector]

    b_edge_1_corner_1.mate_with(b_edge_2_corner_1)
    b_edge_1_corner_2.mate_with(b_edge_2_corner_2)
    b_edge_3_corner_1.mate_with(b_edge_4_corner_1)
    b_edge_3_corner_2.mate_with(b_edge_4_corner_2)

    assert b_edge_1.is_complete()
    assert b_edge_2.is_complete()
    assert b_edge_3.is_complete()
    assert b_edge_4.is_complete()
    assert not b_panel.is_complete()

    # Make sure all edges are parallel to the x, y and z axis.
    c_panel = Panel(Orientation.FLOOR, AbsoluteLocation(0, 0, 0))
    c_edge_1 = Edge(c_panel)
    c_edge_2 = Edge(c_panel)
    c_edge_3 = Edge(c_panel)
    c_edge_4 = Edge(c_panel)
    c_panel.edges = [c_edge_1, c_edge_2, c_edge_3, c_edge_4]
    c_edge_1_corner_1 = CornerNode(c_edge_1, RelativeLocation(0, 0, 0))
    c_edge_1_corner_2 = CornerNode(c_edge_1, RelativeLocation(1, 1, 0))
    c_edge_1_connector = ConnectorNode(c_edge_1, RelativeLocation(0.5, 0.5, 0))
    c_edge_1.corner_nodes = [c_edge_1_corner_1, c_edge_1_corner_2]
    c_edge_1.connector_nodes = [c_edge_1_connector]
    c_edge_2_corner_1 = CornerNode(c_edge_2, RelativeLocation(1, 1, 0))
    c_edge_2_corner_2 = CornerNode(c_edge_2, RelativeLocation(1, 0, 0))
    c_edge_2_connector = ConnectorNode(c_edge_2, RelativeLocation(1, 0.5, 0))
    c_edge_2.corner_nodes = [c_edge_2_corner_1, c_edge_2_corner_2]
    c_edge_2.connector_nodes = [c_edge_2_connector]
    c_edge_3_corner_1 = CornerNode(c_edge_3, RelativeLocation(1, 0, 0))
    c_edge_3_corner_2 = CornerNode(c_edge_3, RelativeLocation(0, -1, 0))
    c_edge_3_connector = ConnectorNode(c_edge_3, RelativeLocation(-0.5, -0.5, 0))
    c_edge_3.corner_nodes = [c_edge_3_corner_1, c_edge_3_corner_2]
    c_edge_3.connector_nodes = [c_edge_3_connector]
    c_edge_4_corner_1 = CornerNode(c_edge_4, RelativeLocation(0, -1, 0))
    c_edge_4_corner_2 = CornerNode(c_edge_4, RelativeLocation(0, 0, 0))
    c_edge_4_connector = ConnectorNode(c_edge_4, RelativeLocation(0, -0.5, 0))
    c_edge_4.corner_nodes = [c_edge_4_corner_1, c_edge_4_corner_2]
    c_edge_4.connector_nodes = [c_edge_4_connector]

    c_edge_1_corner_1.mate_with(c_edge_4_corner_2)
    c_edge_2_corner_1.mate_with(c_edge_1_corner_2)
    c_edge_3_corner_1.mate_with(c_edge_2_corner_2)
    c_edge_4_corner_1.mate_with(c_edge_3_corner_2)

    # The edge cannot pass completeness test if it is not parallel to any axis.
    # Thus the panel cannot pass completeness because that requires all of its 
    # edges to pass completeness. 
    with pytest.raises(ValueError):
        c_edge_1.is_complete()
    