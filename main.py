from fastapi import FastAPI, HTTPException
from typing import List
from dev_parcial2.data.models import UserCreate, UserOut
from dev_parcial2.operations import operations_db

app = FastAPI(title="API de Usuarios")

operations_db.init_db()


@app.post("/users", response_model=UserOut)
def create_user(user: UserCreate):
    return operations_db.create_user(user)


@app.get("/users/active", response_model=List[UserOut])
def list_active_users():
    return operations_db.filter_users(is_active=True)


@app.get("/users/premium-active", response_model=List[UserOut])
def list_premium_active_users():
    return operations_db.filter_users(is_active=True, is_premium=True)


# 👇 CAMBIAMOS ESTA RUTA para evitar conflicto
@app.get("/users/id/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    user = operations_db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@app.patch("/users/id/{user_id}/status", response_model=UserOut)
def update_status(user_id: int, is_active: bool):
    updated = operations_db.update_user_field(user_id, "is_active", str(is_active))
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated


@app.patch("/users/id/{user_id}/premium", response_model=UserOut)
def make_premium(user_id: int):
    updated = operations_db.update_user_field(user_id, "is_premium", "True")
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated


@app.delete("/users/id/{user_id}", response_model=UserOut)
def delete_user(user_id: int):
    deleted = operations_db.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return deleted
