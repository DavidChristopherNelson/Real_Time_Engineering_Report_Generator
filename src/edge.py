from .panel import Panel
from src.utility import validate_instance

class Edge:
    def __init__(self, panel):
        validate_instance(panel, Panel)
        self._panel = panel
        self._connector_nodes = []
        self._corner_nodes = []

    # Defining getter and setter methods
    @property
    def panel(self):
        return self._panel
    
    @panel.setter
    def panel(self, value):
        validate_instance(value, Panel)
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
