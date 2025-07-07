from typing import Optional
from datetime import datetime

class Incident:
    def __init__(self, id: str, monitor_id: str, started_at: datetime, status: str, ended_at: Optional[datetime] = None, root_cause: Optional[str] = None, duration_seconds: Optional[int] = None):
        self.id = id
        self.monitor_id = monitor_id
        self.started_at = started_at
        self.status = status
        self.ended_at = ended_at
        self.root_cause = root_cause
        self.duration_seconds = duration_seconds
