from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

# Estados personalizados
class UserState(str, enum.Enum):
    activo = "Activo"
    inactivo = "Inactivo"
    eliminado = "Eliminado"

class TaskState(str, enum.Enum):
    pendiente = "Pendiente"
    en_ejecucion = "En ejecución"
    realizada = "Realizada"
    cancelada = "Cancelada"

# Modelo Usuario
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    state = Column(Enum(UserState), default=UserState.activo)
    premium = Column(Boolean, default=False)

# Modelo Tarea
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    state = Column(Enum(TaskState), default=TaskState.pendiente)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
