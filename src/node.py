from .edge import Edge
from .location import Location
from .utility import validate_instance

class Node:
    _instances = []

    @classmethod
    def instances(cls):
        return cls._instances

    def __init__(self, edge, location = None):
        validate_instance(edge, Edge)
        if location is None:
            location = Location(None, None, None)
        validate_instance(location, Location)
        self._edge = edge
        self._location = location
        self._mate = None
        Node._instances.append(self)

    @property
    def edge(self):
        return self._edge

    @edge.setter
    def edge(self, value):
        validate_instance(value, Edge)
        if type(self) == CornerNode:
            if len(value.corner_nodes) == 2:
                raise OverflowError(f"Cannot add node: {self} to edge: {value} "
                                    f"because this edge already has two corner "
                                    f"nodes.")
            self.edge.corner_nodes.remove(self)
            value.corner_nodes.append(self)
        elif type(self) == ConnectorNode:
            self.edge.connector_nodes.remove(self)
            value.connector_nodes.append(self)
        self._edge = value

    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, value):
        if value is not None and not isinstance(value, Location):
            raise TypeError(f"""Invalid parameter. {value} must be an instance of 
                            Location""")
        self._location = value
    
    @property
    def mate(self):
        return self._mate

class ConnectorNode(Node):
    def __init__(self, edge, location = None): 
        super().__init__(edge, location)
        edge.connector_nodes.append(self)

#    def __str__(self):
#        return f"""Connector Node Object:
#        Belongs to edge: {self._edge}.
#        _location: {self._location}.
#        _mate: {self._mate}"""

    def mate_with(self, mate):
        # Only mate with CornerNode instances or None
        if mate is not None and not isinstance(mate, ConnectorNode):
            raise TypeError(f"""Invalid parameter. {mate} must be an instance 
                            of ConnectorNode or None.""")
        if self == mate:
            raise ValueError("A ConnectorNode instance cannot mate with itself.")
        if mate is not None and self._edge == mate.edge:
            raise ValueError("Nodes have to be on different edges to mate.")
        self._mate = mate

        if mate is None or mate.mate == self:
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
        # It cannot mate with itself. 
        if self == self.mate:
            return False
        # It's mate cannot have the same edge as self. 
        if self.mate is not None and self.edge == self.mate.edge:
            return False
        return True

class CornerNode(Node):
    def __init__(self, edge, location = None):
        if len(edge.corner_nodes) == 2:
            raise OverflowError(f"Cannot add node: {self} to edge: {edge} "
                                f"because this edge already has two corner "
                                f"nodes.")
        super().__init__(edge, location)
        edge.corner_nodes.append(self)

#    def __str__(self):
#        return f"""Corner Node Object: Belongs to edge: ({self._edge}). _location: ({self._location}). _mate: ({self._mate})"""

    def mate_with(self, mate):
        # Only mate with CornerNode instances or None
        if mate is not None and not isinstance(mate, CornerNode):
            raise TypeError(f"""Invalid parameter. {mate} must be an instance
                            of CornerNode or None.""")
        if self == mate:
            raise ValueError("A CornerNode instance cannot mate with itself.")
        if mate is not None and self._edge == mate.edge:
            raise ValueError("""A CornerNode instance cannot mate with another
                             CornerNode instance on the same edge.""")
        self._mate = mate

        # Now update the mate's information
        if mate is None or mate.mate == self:
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
        return True
