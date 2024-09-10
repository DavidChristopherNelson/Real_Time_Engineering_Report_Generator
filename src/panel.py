from .orientation import Orientation
from .location import Location
from .utility import validate_instance, is_perpendicular

class Panel:
    def __init__(self, _orientation, _location = None):
        # Parameter handling and assignment
        validate_instance(_orientation, Orientation)
        if _location is None:
            _location = Location(None, None, None)
        elif not isinstance(_location, Location):
            raise TypeError("""Invalid parameter. Location must be an 
                            an instance of the Location class""")
        self._orientation = _orientation
        self._location = _location
        self._edges = []

#    def __str__(self):
#        return f"""Panel object. _orientation: ({self._orientation}). _location: ({self._location}). _edges: ({self._edges}). """

    # Defining getter and setter methods
    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        validate_instance(value, Orientation)
        self._orientation = value
    
    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        validate_instance(value, Location)
        self._location = value
    
    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, value):
        from .edge import Edge
        # Parameter handling and assignment
        validate_instance(value, list)
        for index, edge in enumerate(value): 
            if not isinstance(edge, Edge):
                raise TypeError(f"""The edge[{index}] parameter is not an Edge 
                                instance.""")
        self._edges = value
    
    # Untested!!!!
    def is_complete(self):
        # Needs to have an orientation
        #print("Needs to have an orientation")
        if not isinstance(self._orientation, Orientation):
            return False
        # Needs to have a location
        #print("Needs to have a location")
        if not isinstance(self._location, Location):
            return False
        # Needs to have exactly four edges
        #print("Needs to have exactly four edges")
        if len(self._edges) != 4:
            return False
        # Those edges need to be complete
        #print("Those edges need to be complete")
        corners = []
        for edge in self._edges:
            if not edge.is_complete():
                return False
            # Collect corner information
            corners.append(edge.corner_nodes[0])
            corners.append(edge.corner_nodes[1])
        # The corners of these edges cannot mate with corners from edges
        # belonging to other panels.
        #print("The corners of these edges cannot mate...")
        for corner in corners:
            if not corner.mate.edge in self._edges:
                return False
        # The two corner nodes in each edge cannot mate with corner nodes from
        # the same edge
        #print("The two corner nodes in each edge cannot mate with corner nodes ...")
        for edge in self._edges:
            corner_1 = edge.corner_nodes[0]
            corner_2 = edge.corner_nodes[1]
            if corner_1.mate.edge == corner_2.mate.edge:
                return False
        # Edges who have mated corner nodes must be perpendicular to each other
        # Refactor alert: This is inefficient code since it performs eight 
        # checks. It is theoretically possible to reduce this to three checks.
        #print("Perpendicularity")
        for edge in self._edges:
            if not is_perpendicular(edge, edge.corner_nodes[0].mate.edge):
                return False
            if not is_perpendicular(edge, edge.corner_nodes[1].mate.edge):
                return False
        return True
