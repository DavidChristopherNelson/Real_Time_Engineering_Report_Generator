from .orientation import Orientation
from .location import Location
from .utility import validate_instance

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