import asyncio
import asyncpg


# Replace these with your PostgreSQL credentials
DB_NAME = "news_database"
USER = "postgres"
PASSWORD = "postgres123"
HOST = "localhost"
PORT = "5432"

async def test_connection():
    conn = await asyncpg.connect(
        user=USER,
        password=PASSWORD,
        database=DB_NAME,
        host='localhost'
    )
    version = await conn.fetchval('SELECT version();')
    print(f"Connected to database. Version: {version}")
    await conn.close()

asyncio.run(test_connection())