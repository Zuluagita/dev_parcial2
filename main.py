from fastapi import FastAPI, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from dev_parcial2.utils.connection_db import init_db, get_session
from dev_parcial2.data.models import User, Task, UserState, TaskState
from dev_parcial2.operations import operations_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

# --------- USUARIOS ---------
@app.post("/users/", response_model=User)
async def add_user(user: User, session: AsyncSession = Depends(get_session)):
    return await operations_db.create_user(session, user)

@app.get("/users/", response_model=list[User])
async def get_active_users(session: AsyncSession = Depends(get_session)):
    return await operations_db.list_active_users(session)

@app.get("/users/active-premium", response_model=list[User])
async def get_active_premium_users(session: AsyncSession = Depends(get_session)):
    return await operations_db.list_active_premium_users(session)

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await operations_db.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{user_id}/status", response_model=User)
async def update_user_status(user_id: int, state: UserState, session: AsyncSession = Depends(get_session)):
    user = await operations_db.update_user_status(session, user_id, state)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{user_id}/premium", response_model=User)
async def mark_premium(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await operations_db.mark_user_premium(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# --------- TAREAS ---------
@app.post("/tasks/", response_model=Task)
async def add_task(task: Task, session: AsyncSession = Depends(get_session)):
    return await operations_db.create_task(session, task)

@app.get("/tasks/", response_model=list[Task])
async def get_all_tasks(session: AsyncSession = Depends(get_session)):
    return await operations_db.list_all_tasks(session)

@app.get("/tasks/user/{user_id}", response_model=list[Task])
async def get_tasks_by_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await operations_db.list_tasks_by_user(session, user_id)

@app.patch("/tasks/{task_id}/status", response_model=Task)
async def update_task_status(task_id: int, state: TaskState, session: AsyncSession = Depends(get_session)):
    task = await operations_db.update_task_state(session, task_id, state)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
