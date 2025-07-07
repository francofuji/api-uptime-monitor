import uuid
from backend.app.database import get_connection
from backend.models.user import User

class UserRepository:
    @staticmethod
    async def find_by_email(email: str):
        conn = await get_connection()
        row = await conn.fetchrow('SELECT * FROM users WHERE email = $1', email.lower())
        await conn.close()
        if row:
            return User(**dict(row))
        return None

    @staticmethod
    async def find_by_id(user_id: str):
        conn = await get_connection()
        row = await conn.fetchrow('SELECT * FROM users WHERE id = $1', user_id)
        await conn.close()
        if row:
            return User(**dict(row))
        return None

    @staticmethod
    async def create(user_data):
        conn = await get_connection()
        user_id = str(uuid.uuid4())
        await conn.execute('''INSERT INTO users (id, email, password_hash, first_name, last_name, organization_id, role) VALUES ($1, $2, $3, $4, $5, $6, $7)''',
            user_id, user_data.email.lower(), user_data.password_hash, user_data.first_name, user_data.last_name, user_data.organization_id, user_data.role)
        await conn.close()
        return user_id

    @staticmethod
    async def update_last_login(user_id: str):
        conn = await get_connection()
        await conn.execute('UPDATE users SET last_login = NOW() WHERE id = $1', user_id)
        await conn.close()
