import uuid
from backend_py.app.database import get_connection
from backend_py.models.monitor import Monitor

class MonitorRepository:
    @staticmethod
    async def create(monitor_data):
        conn = await get_connection()
        monitor_id = str(uuid.uuid4())
        await conn.execute('''INSERT INTO monitors (id, name, url, method, headers, body, timeout, interval_minutes, expected_status_codes, organization_id, created_by, tags, is_active, "group") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)''',
            monitor_id, monitor_data.name, monitor_data.url, monitor_data.method, monitor_data.headers, monitor_data.body, monitor_data.timeout, monitor_data.interval_minutes, monitor_data.expected_status_codes, monitor_data.organization_id, monitor_data.created_by, monitor_data.tags, True, monitor_data.group)
        await conn.close()
        return monitor_id

    @staticmethod
    async def find_by_id(monitor_id: str):
        conn = await get_connection()
        row = await conn.fetchrow('SELECT * FROM monitors WHERE id = $1', monitor_id)
        await conn.close()
        if row:
            return Monitor(**dict(row))
        return None

    @staticmethod
    async def find_by_organization(organization_id: str, is_active: bool = True):
        conn = await get_connection()
        rows = await conn.fetch('SELECT * FROM monitors WHERE organization_id = $1 AND is_active = $2', organization_id, is_active)
        await conn.close()
        return [Monitor(**dict(row)) for row in rows]

    @staticmethod
    async def update(monitor_id: str, updates: dict):
        conn = await get_connection()
        fields = ', '.join([f"{k} = ${i+2}" for i, k in enumerate(updates.keys())])
        values = list(updates.values())
        await conn.execute(f'UPDATE monitors SET {fields}, updated_at = NOW() WHERE id = $1', monitor_id, *values)
        await conn.close()

    @staticmethod
    async def delete(monitor_id: str):
        conn = await get_connection()
        await conn.execute('DELETE FROM monitors WHERE id = $1', monitor_id)
        await conn.close()
