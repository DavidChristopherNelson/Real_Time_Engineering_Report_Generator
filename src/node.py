from .edge import Edge
from .utility import validate_instance

class Node: 
    def __init__(self, edge):
        validate_instance(edge, Edge)
        self.edge = edge

class ConnectorNode(Node):
    def __init__(self, edge): 
        super().__init__(edge)

class CornerNode(Node):
    def __init__(self, edge): 
        super().__init__(edge)