from .edge import Edge
from .location import Location
from .utility import validate_instance

class Node: 
    def __init__(self, edge, location = None):
        validate_instance(edge, Edge)
        if location is None: 
            location = Location(None, None, None)
        validate_instance(location, Location)
        self._edge = edge
        self._location = edge
        self._mate = None
    
    @property
    def edge(self):
        return self._edge

    @property
    def location(self):
        return self._location
    
    @property
    def mate(self):
        return self._mate
    
    def is_complete(self):
        

class ConnectorNode(Node):
    def __init__(self, edge): 
        super().__init__(edge)

    def mate_with(self, mate):
        # Only mate with ConnectorNode instances
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

    def mate_with(self, mate):
        # Only mate with CornerNode instances
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
