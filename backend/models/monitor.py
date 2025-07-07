from typing import Optional, List
from datetime import datetime

class Monitor:
    def __init__(self, id: str, name: str, url: str, method: str, headers: dict, body: Optional[str], timeout: int, interval_minutes: int, expected_status_codes: list, organization_id: str, created_by: str, tags: Optional[List[str]] = None, is_active: bool = True, group: Optional[str] = None, created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        self.id = id
        self.name = name
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body
        self.timeout = timeout
        self.interval_minutes = interval_minutes
        self.expected_status_codes = expected_status_codes
        self.organization_id = organization_id
        self.created_by = created_by
        self.tags = tags or []
        self.is_active = is_active
        self.group = group
        self.created_at = created_at
        self.updated_at = updated_at
