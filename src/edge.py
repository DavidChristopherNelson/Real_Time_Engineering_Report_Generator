from .panel import Panel
from .utility import validate_instance, is_on
from .object_registry import ObjectRegistry

class Edge:
    def __init__(self, panel):
        validate_instance(panel, Panel)
        self._id = ObjectRegistry.generate_id()
        self._panel = panel
        self._connector_nodes = []
        self._corner_nodes = []
        panel.edges.append(self)
        ObjectRegistry.add_object(self)

#    def __str__(self):
#        return f"""Edge object. Belongs to panel: ({self._panel}). _connector_nodes: ({self._connector_nodes}). _corner_nodes: ({self._corner_nodes})"""

    # Defining getter and setter methods
    @property
    def id(self):
        return self._id

    @property
    def panel(self):
        return self._panel

    @panel.setter
    def panel(self, value):
        validate_instance(value, Panel)
        self._panel.edges.remove(self)
        value.edges.append(self)
        self._panel = value

    @property
    def connector_nodes(self):
        return self._connector_nodes

    @connector_nodes.setter
    def connector_nodes(self, value):
        from .node import ConnectorNode
        validate_instance(value, list)
        for index, connector_node in enumerate(value):
            if not isinstance(connector_node, ConnectorNode): 
                param_type = type(connector_node)
                raise TypeError("""All items in the list must be ConnectorNode 
                                instances. param[{index}] is a {param_type} not 
                                a ConnectorNode.""")
        self._connector_nodes = value
    
    @property
    def corner_nodes(self):
        return self._corner_nodes
    
    @corner_nodes.setter
    def corner_nodes(self, value):
        from .node import CornerNode
        validate_instance(value, list)
        if len(value) > 2:
            raise ValueError("An edge cannot have more than two corner nodes.")
        elif len(value) == 2:
            if value[0] == value[1]:
                raise ValueError("""An edge cannot have two corner nodes be the 
                             same instance""")
        for index, corner_node in enumerate(value):
            if not isinstance(corner_node, CornerNode): 
                param_type = type(corner_node)
                raise TypeError("""All items in the list must be CornerNode 
                                instances. param[{index}] is a {param_type} not 
                                a CornerNode.""")
        self._corner_nodes = value

    # Define other methods
    # This method should only get called on connector node creation.
    def add_connector_nodes(self, value):
        from .node import ConnectorNode
        if (not isinstance(value, list) and 
            not isinstance(value, ConnectorNode)):
            raise TypeError("""Invalid parameter. Parameter must either be a 
                            ConnectorNode instand or be a list of ConnectorNode 
                            instances.""")
        if isinstance(value, ConnectorNode):
            self._connector_nodes.append(value)
        else:
            for index, connector_node in enumerate(value):
                if not isinstance(connector_node, ConnectorNode):
                    param_type = type(connector_node)
                    raise TypeError("""All items in the list must be 
                                    ConnectorNode instances. param[{index}] is 
                                    a {param_type} not a ConnectorNode.""")
                self._connector_nodes.append(connector_node)

    def is_complete(self):
        from .node import Node

        # Needs to belong to a panel
        if not isinstance(self._panel, Panel):
            return False

        # All nodes need to be complete
        for node in self._corner_nodes:
            if not node.is_complete():
                return False
        for node in self._connector_nodes:
            if not node.is_complete():
                return False

        # Needs to have two and only two CornerNodes
        if len(self._corner_nodes) != 2:
            return False

        # These CornerNodes need to have different locations
        if (self._corner_nodes[0].relative_location 
            == self._corner_nodes[1].relative_location):
            return False

        # Needs to have at least one ConnectorNode
        if not self._connector_nodes:
            return False

        # All nodes that point to this edge instance need to be either in 
        # _corner_nodes or _connector_nodes
        for node in Node.instances():
            if node.edge == self:
                if (node not in self._corner_nodes
                    and node not in self._connector_nodes):
                    return False

        # All nodes in _corner_nodes and _connector_nodes need to point to this
        # edge instance. And all nodes need to be complete.
        for node in self._corner_nodes:
            if not node.is_complete:
                return False
            if node.edge != self:
                return False
        for node in self._connector_nodes:
            if not node.is_complete:
                return False
            if node.edge != self:
                return False

        # The location of all nodes in _connector_nodes need to lie on the 
        # geometric line between the two nodes in _corner_nodes
        for node in self._connector_nodes:
            if not is_on(node, self):
                return False

        return True
