from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Dict

class MonitorBase(BaseModel):
    name: str
    url: HttpUrl
    method: str
    headers: Optional[Dict[str, str]] = Field(default_factory=dict)
    body: Optional[str] = None
    timeout: int = 10
    interval_minutes: int = 5
    expected_status_codes: List[int]
    tags: Optional[List[str]] = Field(default_factory=list)
    group: Optional[str] = None

class MonitorCreate(MonitorBase):
    organization_id: str
    created_by: str

class MonitorUpdate(BaseModel):
    name: Optional[str]
    url: Optional[HttpUrl]
    method: Optional[str]
    headers: Optional[Dict[str, str]]
    body: Optional[str]
    timeout: Optional[int]
    interval_minutes: Optional[int]
    expected_status_codes: Optional[List[int]]
    tags: Optional[List[str]]
    group: Optional[str]
    is_active: Optional[bool]

class MonitorOut(MonitorBase):
    id: str
    is_active: bool
    organization_id: str
    created_by: str
    created_at: Optional[str]
    updated_at: Optional[str]
