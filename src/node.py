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
    
    @edge.setter
    def edge(self, value):
        validate_instance(value, Edge)
        self._edge = value

    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, value):
        validate_instance(value, Location)
        self._location = value
    
    @property
    def mate(self):
        return self._mate

class ConnectorNode(Node):
    def __init__(self, edge): 
        super().__init__(edge)

    def mate_with(self, mate):
        # Only mate with ConnectorNode instances
        validate_instance(mate, ConnectorNode)
        if self == mate:
            raise ValueError("A ConnectorNode instance cannot mate with itself.")
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
        if self == mate:
            raise ValueError("A CornerNode instance cannot mate with itself.")
        self._mate = mate
        if mate.mate == self:
            return
        elif mate.mate is None:
            mate.mate_with(self)
        else:
            # Break the mate's existing connection
            mate.mate.mate_with(None)
            mate.mate_with(self)
    
    def is_complete(self):
        # Needs to belong to an edge
        if not isinstance(self._edge, Edge):
            return False
        # Needs to have a non-None Location
        if self._location == Location(None, None, None):
            return False
        # Needs to have a mate. 
        if not isinstance(self._mate, CornerNode):
            return False
        # That mate cannot be itself. 
        if self == self.mate:
            return False
        # That mate cannot have the same edge as self. 
        if self.edge == self.mate.edge:
            return False
        else:
            return True

