"""
The schemas module defines Marshmallow schemas that are shared by various
other serialisation schemas.
"""

from marshmallow.fields import Field, Nested

__all__ = ["UpperCasedField", "NestedDict"]


class UpperCasedField(Field):  # pylint: disable=too-few-public-methods
    """
    Field that serializes to an upper-case string and deserializes
    to a lower-case string.
    """

    def _serialize(self, value, attr, obj, **kwargs):  # pylint: disable=no-self-use
        if value is None:
            return ""
        return value.upper()

    def _deserialize(self, value, attr, data, **kwargs):  # pylint: disable=no-self-use
        return value.lower()


class NestedDict(Nested):
    """
    Field that serialises a list to a dict, with the specified attribute
    acting as key.
    """

    def __init__(self, nested, key, *args, **kwargs):
        super().__init__(nested, many=True, *args, **kwargs)
        self.key = key

    def _serialize(self, nested_obj, attr, obj, **kwargs):
        nested_list = super()._serialize(nested_obj, attr, obj)
        nested_dict = {item[self.key]: item for item in nested_list}
        for item in nested_dict.values():
            del item[self.key]
        return nested_dict

    def _deserialize(self, value, attr, data, partial=None, **kwargs):
        for key, item in value.items():
            item[self.key] = key
        raw_list = [item for key, item in value.items()]
        nested_list = super()._deserialize(raw_list, attr, data)
        return nested_list
