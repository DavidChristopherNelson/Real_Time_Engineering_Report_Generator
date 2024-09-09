import pytest

from src.location import Location

def test_location_initialization():
    location_none = Location(None, None, None)
    assert location_none.x == None
    assert location_none.y == None
    assert location_none.z == None
    location_values = Location(1, 2, 3.0)
    assert location_values.x == 1.0
    assert location_values.y == 2.0
    assert location_values.z == 3.0

def test_invalid_params_location_initialisation():
    with pytest.raises(ValueError):
        location = Location(None, None, "1")
    with pytest.raises(ValueError):
        location = Location(None, None, 1)

def test_equality():
    location = Location(1, 2, 3.0)
    location_2 = Location(1, 2.0, 3)
    location_3 = Location(1, 3, 3)
    location_none = Location(None, None, None)
    location_none_2 = Location(None, None, None)
    assert location == location_2
    assert location != location_3
    assert location != "location_3"
    assert location_none == location_none
