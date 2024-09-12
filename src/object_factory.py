import json

# Assuming you have the following class definitions
from src.panel import Panel
from src.edge import Edge
from src.node import CornerNode, ConnectorNode
from src.location import RelativeLocation
from src.orientation import Orientation
from src.id import ID

def parse_corner_node(edge, corner_node_data):
    id = ID(corner_node_data["id"])
    relative_location = RelativeLocation(corner_node_data["location"]["x"],
                                         corner_node_data["location"]["y"],
                                         corner_node_data["location"]["z"])

    corner_node = CornerNode(id, edge, relative_location)

    if corner_node.is_complete():
        return corner_node
    else:
        raise ValueError(f"Corner node id = {id} is not complete.")
    
def parse_connector_node(edge, connector_node_data):
    id = ID(connector_node_data["id"])
    relative_location = RelativeLocation(connector_node_data["location"]["x"],
                                         connector_node_data["location"]["y"],
                                         connector_node_data["location"]["z"])

    connector_node = ConnectorNode(id, edge, relative_location)

    if connector_node.is_complete():
        return connector_node
    else:
        raise ValueError(f"Connector node id = {id} is not complete.")

def parse_edge(panel, edge_data):
    id = ID(edge_data["id"])
    edge = Edge(id, panel)
    corner_nodes = []

    for corner_node_data in edge_data["corner_nodes"]:
        corner_nodes.append(parse_corner_node(edge, corner_node_data))
    for connector_node_data in edge_data["connector_nodes"]:
        corner_nodes.append(parse_connector_node(edge, connector_node_data))

    if edge.is_complete():
        return edge
    else:
        raise ValueError(f"Edge id = {id} is not complete.")


def parse_panel(panel_data):
    id = ID(panel_data["id"])
    orientation = Orientation(panel_data["orientation"])
    panel = Panel(id, orientation)

    edges = []
    for edge_data in panel_data["edges"]:
        edges.append(parse_edge(panel, edge_data))
    
    # add edges to panel

    if panel.is_complete:
        return panel
    else:
        raise ValueError(f"Panel id = {id} is not complete.")

def load_data_from_json(json_file_name):
    with open(json_file_name, 'r') as file:
        data = json.load(file)

    panels = []
    for panel_data in data["panels"]:
        panels.append(parse_panel(panel_data))
    
    return panels

if __name__ == "__main__":
    panels = load_data_from_json("arduino_data.json")
