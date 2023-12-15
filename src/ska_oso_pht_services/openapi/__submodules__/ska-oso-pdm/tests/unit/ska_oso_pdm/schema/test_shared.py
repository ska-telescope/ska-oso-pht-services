"""
Unit tests for the ska_oso_pdm.schemas.shared module.
"""
from marshmallow import Schema, fields

from ska_oso_pdm.schemas import shared

from ..utils import assert_json_is_equal


def test_upper_cased_field_serialises_to_uppercase():
    """
    Verify that UpperCasedField serialises to uppercase text.
    """

    class TestObject:  # pylint: disable=too-few-public-methods
        """
        Simple test object to hold an attribute.
        """

        def __init__(self):
            self.attr = "bar"

    obj = TestObject()
    serialised = shared.UpperCasedField().serialize("attr", obj)
    assert serialised == "BAR"


def test_upper_cased_field_serialises_none():
    """
    Verify that UpperCasedField serialises None to an empty string.
    """

    class TestObject:  # pylint: disable=too-few-public-methods
        """
        Simple test object to hold an attribute.
        """

        def __init__(self):
            self.attr = None

    obj = TestObject()
    serialised = shared.UpperCasedField().serialize("attr", obj)
    assert serialised == ""


def test_upper_cased_field_deserialises_to_uppercase():
    """
    Verify that UpperCasedField deserialises to lowercase text.
    """
    deserialised = shared.UpperCasedField().deserialize("FOO")
    assert deserialised == "foo"


class Child:  # pylint: disable=invalid-name
    """
    child class holds the arguments
    """

    def __init__(self, id, attr):  # pylint: disable=redefined-builtin
        self.id = id
        self.attr = attr


class Parent:
    """
    Parent class holds the argument
    """

    def __init__(self, children):
        self.children = children


class ChildSchema(Schema):
    """
    child class schema
    """

    id = fields.String()
    attr = fields.String()


class ParentSchema(Schema):
    """
    parent class schema
    """

    children = shared.NestedDict(ChildSchema, key="id")


def test_nesteddict_serialises_list_to_dict():
    """
    verify nested dict serialises list in to dict.
    """
    children = [Child("a", "a val"), Child("b", "b val")]
    parent = Parent(children)

    expected = '{"children": {"a": {"attr": "a val"}, "b": {"attr": "b val"}}}'
    serialised = ParentSchema().dumps(parent)
    assert_json_is_equal(expected, serialised)


def test_nesteddict_deserialises_dict_to_list():
    """
    verify nested dict deserialises dict in to list.
    """
    serialised = '{"children": {"a": {"attr": "a val"}, "b": {"attr": "b val"}}}'
    output = ParentSchema().loads(serialised)
    assert output["children"][0]["id"] == "a"
    assert output["children"][1]["id"] == "b"
