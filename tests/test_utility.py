import pytest

from src.panel import Panel
from src.orientation import Orientation
from src.edge import Edge
from src.location import RelativeLocation, AbsoluteLocation
from src.node import Node, ConnectorNode, CornerNode
from src.utility import (validate_instance, 
                         is_perpendicular, 
                         find_parallel_axis, 
                         is_on,
                         Axis)

def test_validate_instance():
    panel = Panel(Orientation.FLOOR)
    edge = Edge(panel)
    node = Node(edge)
    connector_node = ConnectorNode(edge)
    corner_node = CornerNode(edge)
    relative_location = RelativeLocation()
    absolute_location = AbsoluteLocation()
    orientation = Orientation.FLOOR
    with pytest.raises(TypeError):
        validate_instance(node, Edge)
    with pytest.raises(TypeError):
        validate_instance(edge, Panel)
    with pytest.raises(TypeError):
        validate_instance(panel, RelativeLocation)
    with pytest.raises(TypeError):
        validate_instance(relative_location, Orientation)
    with pytest.raises(TypeError):
        validate_instance(orientation, Node)
    with pytest.raises(TypeError):
        validate_instance(connector_node, CornerNode)
    with pytest.raises(TypeError):
        validate_instance(corner_node, ConnectorNode)

    assert validate_instance(node, Node) == None
    assert validate_instance(connector_node, Node) == None
    assert validate_instance(corner_node, Node) == None
    assert validate_instance(connector_node, ConnectorNode) == None
    assert validate_instance(corner_node, CornerNode) == None
    assert validate_instance(edge, Edge) == None
    assert validate_instance(panel, Panel) == None
    assert validate_instance(relative_location, RelativeLocation) == None
    assert validate_instance(absolute_location, AbsoluteLocation) == None
    assert validate_instance(orientation, Orientation) == None

def test_is_perpendicular():
    # Create a complete panel
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

    assert is_perpendicular(edge_1, edge_2)

    # test paramater validation
    with pytest.raises(TypeError): 
        is_perpendicular("edge_1", "edge_2")
    with pytest.raises(TypeError): 
        is_perpendicular(Edge(panel), "edge_2")
    with pytest.raises(TypeError): 
        is_perpendicular("edge_1", Edge(panel))
    with pytest.raises(ValueError): 
        is_perpendicular(Edge(panel), Edge(panel))
    with pytest.raises(ValueError): 
        is_perpendicular(edge_1, Edge(panel))
    with pytest.raises(ValueError): 
        is_perpendicular(Edge(panel), edge_1)

    # Now construct a parallelagram
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

    with pytest.raises(ValueError):
        is_perpendicular(c_edge_1, c_edge_2)

def test_find_parallel_axis():
    with pytest.raises(TypeError):
        find_parallel_axis("edge")
    panel = Panel(Orientation.FLOOR)
    edge = Edge(panel)
    corner_1 = CornerNode(edge, RelativeLocation(0, 0, 0))
    corner_2 = CornerNode(edge, RelativeLocation(1, 0, 0))
    edge.corner_nodes = [corner_1, corner_2]
    assert find_parallel_axis(edge) == Axis.X
    corner_2.relative_location = RelativeLocation(0, 1, 0)
    assert find_parallel_axis(edge) == Axis.Y
    corner_2.relative_location = RelativeLocation(0, 0, 1)
    assert find_parallel_axis(edge) == Axis.Z
    corner_2.relative_location = RelativeLocation(1, 1, 0)
    with pytest.raises(ValueError):
        find_parallel_axis(edge)
    corner_2.relative_location = RelativeLocation(1, 0, 1)
    with pytest.raises(ValueError):
        find_parallel_axis(edge)
    corner_2.relative_location = RelativeLocation(0, 1, 1)
    with pytest.raises(ValueError):
        find_parallel_axis(edge)
    corner_2.relative_location = RelativeLocation(1, 1, 1)
    with pytest.raises(ValueError):
        find_parallel_axis(edge)

def test_is_on():
    panel = Panel(Orientation.FLOOR)
    edge = Edge(panel)
    origin = RelativeLocation(0,0,0)
    unit_vector_x = RelativeLocation(1,0,0)
    unit_vector_y = RelativeLocation(0,1,0)
    unit_vector_z = RelativeLocation(0,0,1)
    vector_x = RelativeLocation(2,0,0)
    vector_y = RelativeLocation(0,2,0)
    vector_z = RelativeLocation(0,0,2)
    connector_node = ConnectorNode(edge)
    corner_origin = CornerNode(edge, origin)


    # First parameter needs to be a Node instance
    with pytest.raises(TypeError):
        is_on(panel, edge)

    # Second parameter needs to be a Edge instance
    with pytest.raises(TypeError):
        is_on(connector_node, vector_x)

    # Edge needs two corner nodes
    with pytest.raises(ValueError):
        is_on(connector_node, edge)
    corner_node = CornerNode(edge)

    # Edge needs two corner nodes with locations
    corner_node.relative_location = None
    with pytest.raises(ValueError):
        is_on(connector_node, edge)

    # Node needs to have a location
    with pytest.raises(ValueError):
        is_on(connector_node, edge)

    origin = RelativeLocation(0,0,0)
    unit_vector_x = RelativeLocation(1,0,0)
    unit_vector_y = RelativeLocation(0,1,0)
    unit_vector_z = RelativeLocation(0,0,1)
    vector_x = RelativeLocation(2,0,0)
    vector_y = RelativeLocation(0,2,0)
    vector_z = RelativeLocation(0,0,2)

    corner_node.relative_location = vector_x
    connector_node.relative_location = unit_vector_x
    assert is_on(connector_node, edge)

    corner_node.relative_location = vector_y
    connector_node.relative_location = unit_vector_y
    assert is_on(connector_node, edge)

    corner_node.relative_location = vector_z
    connector_node.relative_location = unit_vector_z
    assert is_on(connector_node, edge)

    corner_node.relative_location = vector_y
    connector_node.relative_location = unit_vector_x
    assert not is_on(connector_node, edge)

    corner_node.relative_location = vector_z
    connector_node.relative_location = unit_vector_y
    assert not is_on(connector_node, edge)

    corner_node.relative_location = vector_x
    connector_node.relative_location = unit_vector_z
    assert not is_on(connector_node, edge)
