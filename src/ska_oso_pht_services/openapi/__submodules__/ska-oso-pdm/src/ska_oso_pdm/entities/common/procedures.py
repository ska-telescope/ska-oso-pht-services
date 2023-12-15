"""
The entities.common.procedures module defines a Python representation of the
procedures listed in the activities of the SKA scheduling block.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

__all__ = ["InlineScript", "FilesystemScript", "GitScript"]


class PythonArguments:
    """
    Represents the arguments for a PythonProcedure in an SKA scheduling block.
    """

    def __init__(self, args: List = None, kwargs: Dict = None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        self.args = args
        self.kwargs = kwargs

    def __eq__(self, other):
        return self.args == other.args and self.kwargs == other.kwargs

    def __repr__(self):
        return f"<PythonArguments(" f"args={self.args}, " f"kwargs={self.kwargs})>"


class PythonProcedure(ABC):
    """
    Represents a PythonProcedure to be run as an activity in an SKA scheduling block.
    """

    def __init__(self, function_args: Dict[str, PythonArguments] = None):
        if function_args is None:
            function_args = {}
        self.function_args = function_args

    @property
    @abstractmethod
    def kind(self):
        raise NotImplementedError


class InlineScript(PythonProcedure):
    """
    Represents an InlineScript to be ran as an activity in an SKA scheduling block.
    """

    kind = "inline"

    def __init__(self, content: str, function_args: Dict[str, PythonArguments] = None):
        self.content = content

        super().__init__(function_args)

    def __eq__(self, other):
        if not isinstance(other, InlineScript):
            return False

        return (
            self.content == other.content and self.function_args == other.function_args
        )

    def __repr__(self):
        return (
            f"<InlineScript("
            f"function_args={self.function_args}, "
            f"content={self.content})>"
        )


class FilesystemScript(PythonProcedure):
    """
    Represents an FilesystemScript to be run as an activity in an SKA scheduling block.
    """

    kind = "filesystem"

    def __init__(self, path: str, function_args: Dict[str, PythonArguments] = None):
        self.path = path

        super().__init__(function_args)

    def __eq__(self, other):
        if not isinstance(other, FilesystemScript):
            return False

        return self.path == other.path and self.function_args == other.function_args

    def __repr__(self):
        return (
            f"<FilesystemScript("
            f"function_args={self.function_args}, "
            f"path={self.path})>"
        )


class GitScript(FilesystemScript):
    """
    Represents an GitScript to be run as an activity in an SKA scheduling block.
    """

    kind = "git"

    def __init__(
        self,
        repo: str,
        path: str,
        branch: Optional[str] = None,
        commit: Optional[str] = None,
        function_args: Dict[str, PythonArguments] = None,
    ):  # pylint: disable=too-many-arguments
        self.repo = repo
        self.branch = branch
        self.commit = commit

        super().__init__(path, function_args)

    def __eq__(self, other):
        if not isinstance(other, GitScript):
            return False

        return (
            self.repo == other.repo
            and self.path == other.path
            and self.branch == other.branch
            and self.commit == other.commit
            and self.function_args == other.function_args
        )

    def __repr__(self):
        return (
            f"<GitScript("
            f"function_args={self.function_args}, "
            f"path={self.path}, "
            f"repo={self.repo}, "
            f"branch={self.branch}, "
            f"commit={self.commit})>"
        )
