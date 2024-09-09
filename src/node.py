from .edge import Edge
from .utility import validate_instance

class Node: 
    def __init__(self, edge):
        validate_instance(edge, Edge)
        self.edge = edge

class ConnectorNode(Node):
    def __init__(self, edge): 
        super().__init__(edge)
        self._mate = None

    @property
    def mate(self):
        return self._mate

    def mate_with(self, mate):
        validate_instance(mate, ConnectorNode)
        self._mate = mate
        if mate.mate == self:
            return
        elif mate.mate is None: 
            mate.mate_with(self)
        else:
            # Break the mate's existing connection
            mate.mate.mate_with(None)
            mate.mate_with(self)


class CornerNode(Node):
    def __init__(self, edge): 
        super().__init__(edge)
        self._mate = None

    @property
    def mate(self):
        return self._mate

    def mate_with(self, mate):
        validate_instance(mate, CornerNode)
        self._mate = mate
        if mate.mate == self:
            return
        elif mate.mate is None:
            mate.mate_with(self)
        else:
            # Break the mate's existing connection
            mate.mate.mate_with(None)
            mate.mate_with(self)