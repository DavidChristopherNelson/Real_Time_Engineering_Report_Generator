import pytest

from src.location import RelativeLocation, AbsoluteLocation

def test_relative_location_initialization():
    relative_location_none = RelativeLocation(None, None, None)
    assert relative_location_none.x == None
    assert relative_location_none.y == None
    assert relative_location_none.z == None
    relative_location_values = RelativeLocation(1, 2, 3.0)
    assert relative_location_values.x == 1.0
    assert relative_location_values.y == 2.0
    assert relative_location_values.z == 3.0

def test_invalid_params_relative_location_initialisation():
    with pytest.raises(ValueError):
        relative_location = RelativeLocation(None, None, "1")
    with pytest.raises(ValueError):
        relative_location = RelativeLocation(None, None, 1)

def test_relative_location_equality():
    relative_location = RelativeLocation(1, 2, 3.0)
    relative_location_2 = RelativeLocation(1, 2.0, 3)
    relative_location_3 = RelativeLocation(1, 3, 3)
    relative_location_none = RelativeLocation(None, None, None)
    relative_location_none_2 = RelativeLocation(None, None, None)
    absolute_location = AbsoluteLocation(1, 2, 3.0)
    assert relative_location == relative_location_2
    assert relative_location != relative_location_3
    assert relative_location != "location_3"
    assert relative_location != absolute_location

def test_absolute_location_initialization():
    absolute_location_none = AbsoluteLocation(None, None, None)
    assert absolute_location_none.x == None
    assert absolute_location_none.y == None
    assert absolute_location_none.z == None
    absolute_location_values = AbsoluteLocation(1, 2, 3.0)
    assert absolute_location_values.x == 1.0
    assert absolute_location_values.y == 2.0
    assert absolute_location_values.z == 3.0

def test_invalid_params_absolute_location_initialisation():
    with pytest.raises(ValueError):
        absolutelocation = AbsoluteLocation(None, None, "1")
    with pytest.raises(ValueError):
        absolutelocation = AbsoluteLocation(None, None, 1)

def test_absolute_location_equality():
    absolute_location = AbsoluteLocation(1, 2, 3.0)
    absolute_location_2 = AbsoluteLocation(1, 2.0, 3)
    absolute_location_3 = AbsoluteLocation(1, 3, 3)
    absolute_location_none = AbsoluteLocation(None, None, None)
    absolute_location_none_2 = AbsoluteLocation(None, None, None)
    relative_location = RelativeLocation(1, 2, 3.0)
    assert absolute_location == absolute_location_2
    assert absolute_location != absolute_location_3
    assert absolute_location != "absolute_location_3"
    assert absolute_location != relative_location
