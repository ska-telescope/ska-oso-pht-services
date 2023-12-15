"""
The schemas.common.procedures defines Marshmallow schema that map the
activities section of an SKA scheduling block to/from a JSON
representation.
"""

from marshmallow import Schema, fields, post_dump, post_load
from marshmallow_oneofschema import OneOfSchema

from ...entities.common.procedures import (
    FilesystemScript,
    GitScript,
    InlineScript,
    PythonArguments,
    PythonProcedure,
)


class PythonArgumentsSchema(Schema):
    """
    Schema for the PythonArguments, used in the activities section of an SKA scheduling block
    """

    args = fields.List(fields.String())
    kwargs = fields.Dict()

    @post_load
    def make_pythonarguments(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a PythonArguments object.
        """
        args = data["args"]
        kwargs = data["kwargs"]

        return PythonArguments(args, kwargs)


class InlineScriptSchema(Schema):
    """
    Schema for an InlineScript, used in the activities section of an SKA scheduling block
    """

    kind = fields.String(required=True)
    function_args = fields.Dict(fields.String(), fields.Nested(PythonArgumentsSchema))
    content = fields.String()

    @post_load
    def make_embeddedscript(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a EmbeddedScript object.
        """
        function_args = data["function_args"]
        content = data["content"]
        return InlineScript(content, function_args)


class FileSystemScriptSchema(Schema):
    """
    Schema for a FilesystemScript, used in the activities section of an SKA scheduling block
    """

    kind = fields.String(required=True)
    function_args = fields.Dict(fields.String(), fields.Nested(PythonArgumentsSchema))
    path = fields.String()

    @post_load
    def make_filesystemscript(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a FilesystemScript object.
        """
        function_args = data["function_args"]
        path = data["path"]
        return FilesystemScript(path, function_args)


class GitScriptSchema(Schema):
    """
    Schema for a GitScript, used in the activities section of an SKA scheduling block
    """

    kind = fields.String(required=True)
    function_args = fields.Dict(fields.String(), fields.Nested(PythonArgumentsSchema))
    path = fields.String()
    repo = fields.String()
    branch = fields.String()
    commit = fields.String()

    @post_load
    def make_gitscript(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a GitScript object.
        """
        # do not pass kind as that's a requirement of the JSON and not needed by the class
        return GitScript(**{k: v for k, v in data.items() if k != "kind"})

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}


class PythonProcedureSchema(OneOfSchema):
    """
    Schema for an abstract PythonProcedure, used in the activities
    section of an SKA scheduling block
    """

    type_field = "kind"
    # kind is a required field of the implementing subclasses so do not remove it
    type_field_remove = False
    type_schemas = {
        InlineScript.kind: InlineScriptSchema,
        FilesystemScript.kind: FileSystemScriptSchema,
        GitScript.kind: GitScriptSchema,
    }

    def get_obj_type(self, obj):
        if isinstance(obj, PythonProcedure):
            return obj.kind

        raise Exception(f"Unknown object type: {obj.__class__.__name__}")
