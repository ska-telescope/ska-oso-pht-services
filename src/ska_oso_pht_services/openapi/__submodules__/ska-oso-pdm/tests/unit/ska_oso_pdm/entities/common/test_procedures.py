"""
Unit tests for the ska_oso_pdm.entities.common.procedures module.
"""

from ska_oso_pdm.entities.common.procedures import (
    FilesystemScript,
    GitScript,
    InlineScript,
    PythonArguments,
)


def test_embeddedscript_eq():
    """
    Verify that EmbeddedScript objects are considered equal when the fields are equal.
    """
    embedded_script = InlineScript(
        content="the script content",
        function_args={
            "first": PythonArguments(args=["one arg"], kwargs={"argname": "argval"})
        },
    )

    assert embedded_script == InlineScript(
        content="the script content",
        function_args={
            "first": PythonArguments(args=["one arg"], kwargs={"argname": "argval"})
        },
    )


def test_embeddedscript_not_equal_to_other_objects():
    """
    Verify that EmbeddedScript objects are considered unequal to other objects.
    """
    embedded_script = InlineScript(
        content="the script content",
        function_args={
            "first": PythonArguments(args=["one arg"], kwargs={"argname": "argval"})
        },
    )

    assert embedded_script != object
    assert embedded_script != InlineScript(content="the script content")


def test_file_system_script_eq():
    """
    Verify that FilesystemScript objects are considered equal when the fields are equal.
    """
    file_system_script = FilesystemScript(
        path="/path/to/script.py",
        function_args={
            "first": PythonArguments(args=["one arg"], kwargs={"argname": "argval"})
        },
    )

    assert file_system_script == FilesystemScript(
        path="/path/to/script.py",
        function_args={
            "first": PythonArguments(args=["one arg"], kwargs={"argname": "argval"})
        },
    )


def test_file_system_script_not_equal_to_other_objects():
    """
    Verify that FilesystemScript objects are considered unequal to other objects.
    """
    file_system_script = FilesystemScript(
        path="/path/to/script.py",
        function_args={
            "first": PythonArguments(args=["one arg"], kwargs={"argname": "argval"})
        },
    )

    assert file_system_script != object
    assert file_system_script != FilesystemScript(path="/path/to/script.py")


def test_git_script_eq():
    """
    Verify that GitScript objects are considered equal when the fields are equal.
    """
    git_script = GitScript(
        repo="http://repo",
        path="path/inside/repo",
        branch="main",
        commit="dbf8447fee57581a722e3d24582ca14cbba1f90f",
        function_args={
            "first": PythonArguments(args=["one arg"], kwargs={"argname": "argval"})
        },
    )

    assert git_script == GitScript(
        repo="http://repo",
        path="path/inside/repo",
        branch="main",
        commit="dbf8447fee57581a722e3d24582ca14cbba1f90f",
        function_args={
            "first": PythonArguments(args=["one arg"], kwargs={"argname": "argval"})
        },
    )


def test_git_script_not_equal_to_other_objects():
    """
    Verify that GitScript objects are considered unequal to other objects.
    """
    git_script = GitScript(
        repo="http://repo",
        path="path/inside/repo",
        branch="main",
        commit="dbf8447fee57581a722e3d24582ca14cbba1f90f",
        function_args={
            "first": PythonArguments(args=["one arg"], kwargs={"argname": "argval"})
        },
    )

    assert git_script != object
    assert git_script != GitScript(
        repo="http://repo",
        path="path/inside/repo",
    )
