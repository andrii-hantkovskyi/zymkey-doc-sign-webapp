import asyncpg
from settings import DATABASE_URL


async def get_connection():
    return await asyncpg.connect(DATABASE_URL)


async def get_user(username: str):
    conn = await get_connection()
    row = await conn.fetchrow(
        "SELECT username, hashed_password, is_admin FROM users WHERE username=$1",
        username,
    )
    await conn.close()
    if row:
        return dict(row)
    return None


async def create_user(username: str, hashed_password: str, is_admin: bool):
    conn = await get_connection()
    await conn.execute(
        "INSERT INTO users (username, hashed_password, is_admin) VALUES ($1, $2, $3)",
        username,
        hashed_password,
        is_admin,
    )
    await conn.close()
