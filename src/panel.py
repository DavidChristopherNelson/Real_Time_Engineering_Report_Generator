from .orientation import Orientation
from .location import Location

class Panel:
    def __init__(self, _orientation, _location = None):
        # Parameter handling and assignment
        if not isinstance(_orientation, Orientation):
            raise TypeError("""Invalid parameter. Orientation must be an 
                            an instance of the Orientation class""")
        if _location is None:
            _location = Location(None, None, None)
        elif not isinstance(_location, Location):
            raise TypeError("""Invalid parameter. Location must be an 
                            an instance of the Location class""")
        self._orientation = _orientation
        self._location = _location
        self._edges = []

    
    # Defining getter and setter methods
    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        if not isinstance(value, Orientation):
            raise TypeError("""Invalid parameter. Orientation must be an 
                            an instance of the Orientation class""")
        self._orientation = value
    
    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        if not isinstance(value, Location):
            raise TypeError("""Invalid parameter. Location must be an 
                            an instance of the Location class""")
        self._location = value
    
    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, value):
        from .edge import Edge
        # Parameter handling and assignment
        if not isinstance(value, list): 
            raise TypeError("""Invalid parameter. Edges must be an 
                            a List of Edge instances.""")
        for index, edge in enumerate(value): 
            if not isinstance(edge, Edge):
                raise TypeError(f"""The edge[{index}] parameter is not an Edge 
                                instance.""")
        self._edges = value