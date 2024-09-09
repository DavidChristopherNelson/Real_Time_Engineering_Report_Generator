from .edge import Edge

class Node: 
    def __init__(self, edge):
        if not isinstance(edge, Edge):
            raise TypeError("""Invalid parameter. Edge must be an 
                            an instance of the Edge class""")
        self.edge = edge

class ConnectorNode(Node):
    def __init__(self, edge): 
        super().__init__(edge)

class CornerNode(Node):
    def __init__(self, edge): 
        super().__init__(edge)