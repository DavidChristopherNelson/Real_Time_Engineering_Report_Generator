from .edge import Edge
from .location import AbsoluteLocation, RelativeLocation
from .utility import validate_instance
from .object_registry import ObjectRegistry

class Node:
    _instances = []

    @classmethod
    def instances(cls):
        return cls._instances

    def __init__(self, 
                 edge, 
                 relative_location = None, 
                 absolute_location = None):
        validate_instance(edge, Edge)
        if relative_location is None:
            relative_location = RelativeLocation(None, None, None)
        validate_instance(relative_location, RelativeLocation)
        if absolute_location is None:
            absolute_location = AbsoluteLocation(None, None, None)
        validate_instance(absolute_location, AbsoluteLocation)

        self._id = ObjectRegistry.generate_id()
        self._edge = edge
        self._relative_location = relative_location
        self._absolute_location = absolute_location
        self._mate = None
        Node._instances.append(self)
        ObjectRegistry.add_object(self)

    @property
    def id(self):
        return self._id

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
    def relative_location(self):
        return self._relative_location
    
    @relative_location.setter
    def relative_location(self, value):
        if value is not None and not isinstance(value, RelativeLocation):
            raise TypeError(f"Invalid parameter. {value} must be an instance"
                            "of RelativeLocation")
        self._relative_location = value

    @property
    def absolute_location(self):
        return self._absolute_location

    @absolute_location.setter
    def absolute_location(self, value):
        if value is not None and not isinstance(value, AbsoluteLocation):
            raise TypeError(f"Invalid parameter. {value} must be an instance"
                            "of AbsoluteLocation")
        self._absolute_location = value
    
    @property
    def mate(self):
        return self._mate

class ConnectorNode(Node):
    def __init__(self, 
                 edge, 
                 relative_location = None, 
                 absolute_location = None): 
        super().__init__(edge, relative_location, absolute_location)
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
            raise ValueError("A ConnectorNode instance cannot mate with "
                             "itself.")
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
        # Needs to have a non-None relative location
        if self._relative_location == RelativeLocation(None, None, None):
            return False
        # It cannot mate with itself. 
        if self == self.mate:
            return False
        # It's mate cannot have the same edge as self. 
        if self.mate is not None and self.edge == self.mate.edge:
            return False
        return True

class CornerNode(Node):
    def __init__(self, 
                 edge, 
                 relative_location = None, 
                 absolute_location = None):
        if len(edge.corner_nodes) == 2:
            raise OverflowError(f"Cannot add node: {self} to edge: {edge} "
                                f"because this edge already has two corner "
                                f"nodes.")
        super().__init__(edge, relative_location, absolute_location)
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
        # Needs to have a non-None relative location
        if self._relative_location == RelativeLocation(None, None, None):
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
