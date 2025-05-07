import os
from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

# Cargar variables del archivo .env
load_dotenv()

# Construir URL de conexión MySQL asincrónica (aiomysql)
DATABASE_URL = (
    f"mysql+aiomysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
    f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
)

# Crear el motor asincrónico
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

# Crear la fábrica de sesiones asincrónicas
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Inicializar las tablas en la base de datos
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Obtener una sesión asincrónica para usar en los endpoints
async def get_session():
    async with async_session() as session:
        yield session
