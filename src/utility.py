from enum import Enum

class Axis(Enum):
    X = "x"
    Y = "y"
    Z = "z"

def validate_instance(value, expected_type):
    if not isinstance(value, expected_type):
        raise TypeError(f"""Invalid parameter. {value} must be an instance of 
                        {expected_type.__name__}""")

def is_perpendicular(edge_1, edge_2):
    from .edge import Edge
    validate_instance(edge_1, Edge)
    validate_instance(edge_2, Edge)
    if not edge_1.is_complete():
        raise ValueError("""Invalid first parameter. The edge needs to be
                        complete.""")
    if not edge_2.is_complete():
        raise ValueError("""Invalid second parameter. The edge needs to be
                        complete.""")
    return find_parallel_axis(edge_1) != find_parallel_axis(edge_2)

# Untested!!!!!!!
def find_parallel_axis(edge):
    from .edge import Edge
    validate_instance(edge, Edge)
    corner_1_location = edge.corner_nodes[0].location
    corner_2_location = edge.corner_nodes[1].location

    delta_x = corner_2_location.x - corner_1_location.x
    delta_y = corner_2_location.y - corner_1_location.y
    delta_z = corner_2_location.z - corner_1_location.z
    zero_count = [delta_x, delta_y, delta_z].count(0)

    if zero_count != 2:
        raise ValueError("This edge is not parallel to any axis.")
    if delta_x != 0:
        return Axis.X
    if delta_y != 0:
        return Axis.Y
    if delta_z != 0:
        return Axis.Z
    
    # This line should not be reached. 
    raise ValueError("Unexpected error in determining the parallel axis.")

def is_on(point, edge):
    from .edge import Edge
    from .node import Node
    validate_instance(point, Node)
    validate_instance(edge, Edge)
    if None == point.location.x == point.location.y == point.location.z:
        raise ValueError("""Invalid first parameter. The node needs to have a 
                         location.""")
    if len(edge.corner_nodes) < 2:
        raise ValueError("""Invalid second parameter. The edge needs two corner
                         nodes.""")
    if edge.corner_nodes[0] == edge.corner_nodes[1]:
        raise ValueError("""Invalid second parameter. The edge needs two corner
                         nodes that are different.""")
    if ((None == edge.corner_nodes[0].location.x 
        == edge.corner_nodes[0].location.y 
        == edge.corner_nodes[0].location.z)
        or 
        (None == edge.corner_nodes[1].location.x 
        == edge.corner_nodes[1].location.y 
        == edge.corner_nodes[1].location.z)):
        raise ValueError("""Invalid second parameter. The edge needs corner
                         nodes that have non-None locations.""")
    corner_1_location = edge.corner_nodes[0].location
    corner_2_location = edge.corner_nodes[1].location
    axis = find_parallel_axis(edge)
    if axis == Axis.X:
        return ((corner_1_location.x < point.location.x < corner_2_location.x)
            or (corner_2_location.x < point.location.x < corner_1_location.x))
    elif axis == Axis.Y:
        return (corner_1_location.y < point.location.y < corner_2_location.y
            or corner_2_location.y < point.location.y < corner_1_location.y)
    elif axis == Axis.Z:
        return (corner_1_location.z < point.location.z < corner_2_location.z
            or corner_2_location.z < point.location.z < corner_1_location.z)
    else:
        raise ValueError("Unexpected value for axis.")
