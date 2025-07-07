import uuid
from datetime import datetime
from backend_py.app.database import get_connection
from backend_py.models.monitor_result import MonitorResult

class MonitorResultRepository:
    @staticmethod
    async def create(result_data):
        conn = await get_connection()
        result_id = str(uuid.uuid4())
        await conn.execute('''INSERT INTO monitor_results (id, monitor_id, response_time_ms, status_code, success, error_message, response_size, location, checked_at, ssl_expiry_date) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)''',
            result_id, result_data.monitor_id, result_data.response_time_ms, result_data.status_code, result_data.success, result_data.error_message, result_data.response_size, result_data.location, result_data.checked_at, result_data.ssl_expiry_date)
        await conn.close()
        return result_id

    @staticmethod
    async def get_latest_results(monitor_id: str, limit: int = 100):
        conn = await get_connection()
        rows = await conn.fetch('SELECT * FROM monitor_results WHERE monitor_id = $1 ORDER BY checked_at DESC LIMIT $2', monitor_id, limit)
        await conn.close()
        return [MonitorResult(**dict(row)) for row in rows]
