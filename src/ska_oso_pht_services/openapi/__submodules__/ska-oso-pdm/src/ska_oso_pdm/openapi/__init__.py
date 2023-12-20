import json
from typing import Type, Union

from ska_oso_pdm.generated.encoder import JSONEncoder
from ska_oso_pdm.generated.models.execution_block import ExecutionBlock
from ska_oso_pdm.generated.models.observing_programme import ObservingProgramme
from ska_oso_pdm.generated.models.project import Project
from ska_oso_pdm.generated.models.sb_definition import SBDefinition
from ska_oso_pdm.generated.models.sb_instance import SBInstance

OSOEntity = Union[SBDefinition, SBInstance, ObservingProgramme, ExecutionBlock, Project]


class OpenAPICodec:
    """
    OpenAPICodec serialises and deserialises OSO entities using a model
    genereated from the OpenAPI spec.
    """

    # pylint: disable=bad-staticmethod-argument
    @staticmethod
    def loads(cls: Type[OSOEntity], json_data: str) -> OSOEntity:
        return cls.from_dict(json.loads(json_data))

    @staticmethod
    def dumps(entity: OSOEntity) -> str:
        return json.dumps(entity, cls=JSONEncoder)


CODEC = OpenAPICodec()
