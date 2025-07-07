import uuid
from datetime import datetime
from backend_py.app.database import get_connection
from backend_py.models.incident import Incident

class IncidentRepository:
    @staticmethod
    async def create(incident_data):
        conn = await get_connection()
        incident_id = str(uuid.uuid4())
        await conn.execute('''INSERT INTO incidents (id, monitor_id, started_at, status) VALUES ($1, $2, $3, $4)''',
            incident_id, incident_data.monitor_id, incident_data.started_at, incident_data.status)
        await conn.close()
        return incident_id

    @staticmethod
    async def resolve(incident_id: str, ended_at: datetime, root_cause: str = None):
        conn = await get_connection()
        await conn.execute('''UPDATE incidents SET ended_at = $2, status = 'resolved', root_cause = $3, duration_seconds = EXTRACT(EPOCH FROM $2 - started_at)::integer WHERE id = $1''',
            incident_id, ended_at, root_cause)
        await conn.close()

    @staticmethod
    async def find_active_by_monitor(monitor_id: str):
        conn = await get_connection()
        rows = await conn.fetch('SELECT * FROM incidents WHERE monitor_id = $1 AND status = $2 ORDER BY started_at DESC', monitor_id, 'open')
        await conn.close()
        return [Incident(**dict(row)) for row in rows]
