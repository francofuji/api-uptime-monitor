from typing import Optional
from datetime import datetime

class MonitorResult:
    def __init__(self, id: str, monitor_id: str, response_time_ms: int, status_code: int, success: bool, error_message: Optional[str], response_size: Optional[int], location: str, checked_at: datetime, ssl_expiry_date: Optional[datetime] = None):
        self.id = id
        self.monitor_id = monitor_id
        self.response_time_ms = response_time_ms
        self.status_code = status_code
        self.success = success
        self.error_message = error_message
        self.response_size = response_size
        self.location = location
        self.checked_at = checked_at
        self.ssl_expiry_date = ssl_expiry_date
