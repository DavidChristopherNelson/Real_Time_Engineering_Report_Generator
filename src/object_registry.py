import uuid
from .utility import validate_instance

class ObjectRegistry:
    _objects_by_id = {}

    @classmethod
    def add_object(cls, obj):
        from .panel import Panel
        from .edge import Edge
        from .node import Node, CornerNode, ConnectorNode
        if (not isinstance(obj, Panel)
            and not isinstance(obj, Edge)
            and not isinstance(obj, Node)
            and not isinstance(obj, CornerNode)
            and not isinstance(obj, ConnectorNode)):
          raise TypeError(f"{obj} is not an instance of Panel, Edge, "
                          "CornerNode or ConnectorNode.")
        cls._objects_by_id[obj.id] = obj

    @classmethod
    def get_object_by_id(cls, id):
        return cls._objects_by_id.get(id)

    @classmethod
    def remove_object_by_id(cls, id):
        if id in cls._objects_by_id:
            del cls._objects_by_id[id]

    @classmethod
    def size(cls):
        return len(cls._objects_by_id)

    @classmethod
    def is_unique(cls, id):
        validate_instance(id, uuid.UUID)
        if id in cls._objects_by_id.keys():
            return False
        return True

    @classmethod
    def generate_id(cls):
        new_id = uuid.uuid4()
        retry_count = 0
        max_retries = 1000000
        while (not cls.is_unique(new_id) and retry_count < max_retries):
            retry_count += 1
            new_id = uuid.uuid4()
        return new_id
    

