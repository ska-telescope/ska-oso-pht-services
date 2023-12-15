"""
Defines the models for the proposal preparation tool.
"""
from pydantic import BaseModel, HttpUrl, conint, confloat, EmailStr
from datetime import datetime
from typing import List


class Metadata(BaseModel):
    skauuid: str
    created_by: str
    submitted_by: str
    updated_by: str
    created_date: datetime
    last_updated_date: datetime
    submitted_date: datetime
    status: str


class ScienceJustification(BaseModel):
    document_id: str
    document_name: str
    link: HttpUrl

class SdpItem(BaseModel):
    pipeline: str 
    pramters: str 

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

class ScienceGoal():
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
    abstract: str
    proposal_type: str
    sub_proposal_type: str
    science_category: str
    science_subcategory: str
    science_justification:ScienceJustification
    technical_justification: ScienceJustification
    targets: List[Target]
    investigator: List[Investigator]
    science_goals: ScienceGoal
    data: DataSection
      
class ProposalDefinition(BaseModel):
    metadata: Metadata
    proposal : Proposal