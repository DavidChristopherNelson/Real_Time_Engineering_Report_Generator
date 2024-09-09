class Location: 
    def __init__(self, x = None, y = None, z = None):
        # Parameter handling and assignment
        all_none = x is None and y is None and z is None
        all_numeric = (
            isinstance(x, (int, float)) 
            and isinstance(y, (int, float)) 
            and isinstance(z, (int, float))
        )
        if not all_none and not all_numeric:
            raise ValueError("""Invalid parameters. x, y and z must either 
                             all be int/float or all be None.""")
        if all_numeric:
            x = float(x)
            y = float(y)
            z = float(z)
        self._x = x
        self._y = y
        self._z = z

    # Defining getter and setter methods
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    def __eq__(self, other):
        if not isinstance(other, Location):
            return False
        return self._x == other.x and self._y == other.y and self.z == other.z