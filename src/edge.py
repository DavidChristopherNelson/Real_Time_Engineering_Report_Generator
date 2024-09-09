from .panel import Panel

class Edge:
    def __init__(self, panel):
        if not isinstance(panel, Panel):
            raise TypeError("""Invalid parameter. Panel must be an 
                            an instance of the Panel class""")
        self._panel = panel
        self._connector_nodes = []
        self._corner_nodes = []

    # Defining getter and setter methods
    @property
    def panel(self):
        return self._panel
    
    @panel.setter
    def panel(self, value):
        if not isinstance(value, Panel):
            raise TypeError("""Invalid parameter. Panel must be an 
                            an instance of the Panel class""")
        self._panel = value
    
    @property
    def connector_nodes(self):
        return self._connector_nodes
    
    @connector_nodes.setter
    def connector_nodes(self, value):
        from .node import ConnectorNode
        if not isinstance(value, list):
            raise TypeError("""Invalid parameter. Parameter must be a list of 
                            ConnectorNode instances.""")
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
        if not isinstance(value, list):
            raise TypeError("""Invalid parameter. Parameter must be a list of 
                            CornerNode instances.""")
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

    def add_corner_nodes(self, value):
        from .node import CornerNode
        if (not isinstance(value, list) and 
            not isinstance(value, CornerNode)):
            raise TypeError("""Invalid parameter. Parameter must either be a 
                            CornerNode instand or be a list of CornerNode 
                            instances.""")
        if isinstance(value, CornerNode):
            self._corner_nodes.append(value)
        else:
            for index, corner_node in enumerate(value):
                if not isinstance(corner_node, CornerNode):
                    param_type = type(corner_node)
                    raise TypeError("""All items in the list must be 
                                    CornerNode instances. param[{index}] is 
                                    a {param_type} not a CornerNode.""")
                self._corner_nodes.append(corner_node)
