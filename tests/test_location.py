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