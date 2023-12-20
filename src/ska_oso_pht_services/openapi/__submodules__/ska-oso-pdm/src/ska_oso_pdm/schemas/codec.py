"""
The codec module contains classes used by clients to marshall PDM classes to
and from JSON. This saves the clients having to instantiate and manipulate the
Marshmallow schema directly.
"""
__all__ = ["MarshmallowCodec"]


class MarshmallowCodec:  # pylint: disable=too-few-public-methods
    """
    MarshmallowCodec marshalls and unmarshalls PDM classes.

    The mapping of PDM classes to Marshmallow schema is defined in this class.
    """

    def __init__(self):
        self._schema = {}

    def register_mapping(self, pdm_class):
        """A decorator that is used to register the mapping between a
        Marshmallow schema and the PDM class it serialises.

        :param pdm_class: the PDM class this schema maps to
        """

        def decorator(class_definition):
            self.set_schema(pdm_class, class_definition)
            return class_definition

        return decorator

    def set_schema(self, pdm_class, schema_class):
        """
        Set the schema for a PDM class.

        :param schema_class: Marshmallow schema to map
        :param pdm_class: PDM class the schema maps to
        """
        self._schema[pdm_class] = schema_class

    def load_from_file(self, cls, path):
        """
        Load an instance of a PDM class from disk.

        :param cls: the class to create from the file
        :param path: the path to the file
        :return: an instance of cls
        """
        with open(path, "r", encoding="utf-8") as json_file:
            json_data = json_file.read()
            return self.loads(cls, json_data)

    def loads(self, pdm_class, json_data):
        """
        Create an instance of a PDM class from a JSON string.

        :param pdm_class: the class to create from the JSON
        :param json_data: the JSON to unmarshall
        :return: an instance of cls
        """
        schema_cls = self._schema[pdm_class]
        schema_obj = schema_cls()
        return schema_obj.loads(json_data=json_data)

    def dumps(self, obj):
        """
        Return a string JSON representation of a PDM instance.

        :param obj: the instance to marshall to JSON
        :return: a JSON string
        """
        schema_cls = self._schema[obj.__class__]
        schema_obj = schema_cls()
        return schema_obj.dumps(obj)
