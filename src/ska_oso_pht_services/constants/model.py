"""
Defines the basic data models for the proposal preparation tool.
"""

from datetime import datetime as dt
from typing import List, Optional, Set

from pydantic import BaseModel, EmailStr, confloat

# TO DO: Add validations where necessary


class MetaData(BaseModel):
    skauuid: str
    created_by: str
    submitted_by: str
    updated_by: Optional[str]
    created_date: dt
    updated_date: Optional[dt]
    submitted_date: Optional[dt]
    status: str


class ScienceJustification(BaseModel):
    document_id: str
    document_name: str
    link: str


class SdpItem(BaseModel):
    pipeline: str
    prameters: str


class DataSection(BaseModel):
    sdp: List[SdpItem]
    src_net: List[SdpItem]


class Target(BaseModel):
    target_id: str
    name: str
    right_ascension: str
    declination: str
    velocity: confloat(ge=0.0)


class Investigator(BaseModel):
    investigator_id: str
    first_name: str
    last_name: str
    email: EmailStr
    country: str
    organization_id: str
    for_phd: str
    has_phd: str
    principal_investigator: str


class ScienceGoal(BaseModel):
    science_goal_id: str
    array: str
    subarray: str
    linked: int
    observation_type: str
    observing_band: str


class Proposal(BaseModel):
    skao_proposal_id: str
    title: str
    cycle: str
    abstract: Optional[str]
    proposal_type: str
    sub_proposal_type: str
    science_category: Optional[str]
    science_subcategory: Optional[str]
    science_justification: Optional[ScienceJustification]
    technical_justification: Optional[ScienceJustification]
    targets: Optional[List[Target]]
    investigator: List[Investigator]
    science_goals: Optional[list[ScienceGoal]]
    # data: DataSection


# class ProposalDefinition(BaseModel):
#     meta_data: MetaData
#     proposal: Proposal


class ProposalDefinition(BaseModel):
    meta_data: MetaData
    investigator: Set[str]
    proposal: dict
