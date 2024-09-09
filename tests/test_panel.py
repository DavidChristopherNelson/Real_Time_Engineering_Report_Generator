import pytest

from src.panel import Panel
from src.orientation import Orientation
from src.location import Location
from src.edge import Edge

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
    assert panel.location.x == None
    assert panel.location.y == None
    assert panel.location.z == None

def test_panel_location_initialization():
    panel = Panel(Orientation.FLOOR, Location(1, 2, 3))
    assert panel.location.x == 1
    assert panel.location.y == 2
    assert panel.location.z == 3

def test_invalid_params_panel_initialisation():
    with pytest.raises(TypeError):
        panel = Panel("floor")
    with pytest.raises(TypeError):
        location = [1, 2, 3]
        panel = Panel(Orientation.FLOOR, location)

# Panel Method Tests
def test_edges_setter_and_getter():
    panel = Panel(Orientation.FLOOR, Location(1, 2, 3))
    edge_1 = Edge(panel)
    edge_2 = Edge(panel)
    edge_3 = Edge(panel)
    edge_4 = Edge(panel)
    edges = [edge_1, edge_2, edge_3, edge_4]
    panel.edges = edges
    assert panel.edges[0] == edge_1
    assert panel.edges[1] == edge_2
    assert panel.edges[2] == edge_3
    assert panel.edges[3] == edge_4