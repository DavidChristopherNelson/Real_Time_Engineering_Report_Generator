class Location: 
    def __init__(self, _x, _y, _z):
        # Parameter handling and assignment
        all_none = _x is None and _y is None and _z is None
        all_numeric = (
            isinstance(_x, (int, float)) 
            and isinstance(_y, (int, float)) 
            and isinstance(_z, (int, float))
        )
        if not all_none and not all_numeric:
            raise ValueError("""Invalid parameters. x, y and z must either 
                             all be int/float or all be None.""")
        self.x = _x
        self.y = _y
        self.z = _z

        # Defining getter and setter methods
        @property
        def x(self):
            self._x

        @x.setter
        def x(self, value):
            self._x = value

        @property
        def y(self):
            self._y

        @y.setter
        def y(self, value):
            self._y = value

        @property
        def z(self):
            self._z

        @z.setter
        def z(self, value):
            self._z = value