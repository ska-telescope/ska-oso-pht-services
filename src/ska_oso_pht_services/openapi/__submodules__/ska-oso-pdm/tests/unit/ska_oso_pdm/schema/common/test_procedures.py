"""
tests for the procedures_schema to validate the
conversion between the JSON and Python representations
of the activities section of an SKA Scheduling Block
"""

from ska_oso_pdm.entities.common.procedures import (
    FilesystemScript,
    GitScript,
    InlineScript,
    PythonArguments,
)
from ska_oso_pdm.schemas.common.procedures import PythonProcedureSchema
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal

VALID_INLINESCRIPT_JSON = """
{
  "kind": "inline",
  "function_args": {
    "first": {
        "args": ["one arg"],
        "kwargs": {}
      }
  },
  "content": "the script content"
}
"""

VALID_FILESYSTEM_SCRIPT_JSON = """
{
  "kind": "filesystem",
  "function_args": {
    "first": {
        "args": [],
        "kwargs": {
            "one": "kwarg"
        }
      }
  },
  "path": "/path/to/script.py"
}
"""

VALID_GITSCRIPT_JSON = """
{
  "kind": "git",
  "function_args": {
    "first": {
        "args": [],
        "kwargs": {
            "one": "kwarg"
        }
      }
  },
  "path": "/path/to/script.py",
  "repo": "http://repo",
  "branch": "main",
  "commit": "dbf8447fee57581a722e3d24582ca14cbba1f90f"
}
"""


def test_marshall_embedded_script_to_json():
    """
    Verify that an EmbeddedScript is marshalled to JSON correctly.
    """
    embedded_script = InlineScript(
        content="the script content",
        function_args={"first": PythonArguments(args=["one arg"])},
    )

    json_str = PythonProcedureSchema().dumps(embedded_script)

    assert_json_is_equal(json_str, VALID_INLINESCRIPT_JSON)


def test_unmarshall_embedded_script_from_json():
    """
    Verify that an EmbeddedScript is unmarshalled correctly from JSON.
    """
    expected = InlineScript(
        content="the script content",
        function_args={"first": PythonArguments(args=["one arg"])},
    )
    unmarshalled = PythonProcedureSchema().loads(VALID_INLINESCRIPT_JSON)
    assert unmarshalled == expected


def test_marshall_filesystem_script_to_json():
    """
    Verify that a FilesystemScript is marshalled to JSON correctly.
    """
    filesystem_script = FilesystemScript(
        path="/path/to/script.py",
        function_args={"first": PythonArguments(kwargs={"one": "kwarg"})},
    )

    json_str = PythonProcedureSchema().dumps(filesystem_script)

    assert_json_is_equal(json_str, VALID_FILESYSTEM_SCRIPT_JSON)


def test_unmarshall_filesystem_script_from_json():
    """
    Verify that a FilesystemScript is unmarshalled correctly from JSON.
    """
    expected = FilesystemScript(
        path="/path/to/script.py",
        function_args={"first": PythonArguments(kwargs={"one": "kwarg"})},
    )
    unmarshalled = PythonProcedureSchema().loads(VALID_FILESYSTEM_SCRIPT_JSON)
    assert unmarshalled == expected


def test_marshall_git_script_to_json():
    """
    Verify that a GitScript is marshalled to JSON correctly.
    """
    git_script = GitScript(
        path="/path/to/script.py",
        repo="http://repo",
        branch="main",
        commit="dbf8447fee57581a722e3d24582ca14cbba1f90f",
        function_args={"first": PythonArguments(kwargs={"one": "kwarg"})},
    )

    json_str = PythonProcedureSchema().dumps(git_script)

    assert_json_is_equal(json_str, VALID_GITSCRIPT_JSON)


def test_unmarshall_git_script_from_json():
    """
    Verify that a DriftScanTarget is unmarshalled correctly from JSON.
    """
    expected = GitScript(
        path="/path/to/script.py",
        repo="http://repo",
        branch="main",
        commit="dbf8447fee57581a722e3d24582ca14cbba1f90f",
        function_args={"first": PythonArguments(kwargs={"one": "kwarg"})},
    )
    unmarshalled = PythonProcedureSchema().loads(VALID_GITSCRIPT_JSON)
    assert unmarshalled == expected
