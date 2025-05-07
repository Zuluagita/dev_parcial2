from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import enum

class UserState(str, enum.Enum):
    activo = "Activo"
    inactivo = "Inactivo"
    eliminado = "Eliminado"

class TaskState(str, enum.Enum):
    pendiente = "Pendiente"
    en_ejecucion = "En ejecución"
    realizada = "Realizada"
    cancelada = "Cancelada"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    state: UserState = Field(default=UserState.activo)
    premium: bool = Field(default=False)

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    state: TaskState = Field(default=TaskState.pendiente)
    user_id: int = Field(foreign_key="user.id")
