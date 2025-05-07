from sqlmodel import select
from ..data.models import User, Task, UserState, TaskState

# --------- USUARIOS ---------
async def create_user(session, user_data):
    user = User(**user_data.dict())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user_by_id(session, user_id: int):
    return await session.get(User, user_id)

async def update_user_status(session, user_id: int, new_state: UserState):
    user = await get_user_by_id(session, user_id)
    if user:
        user.state = new_state
        await session.commit()
        await session.refresh(user)
    return user

async def mark_user_premium(session, user_id: int):
    user = await get_user_by_id(session, user_id)
    if user:
        user.premium = True
        await session.commit()
        await session.refresh(user)
    return user

async def list_active_users(session):
    result = await session.execute(select(User).where(User.state == UserState.activo))
    return result.scalars().all()

async def list_active_premium_users(session):
    result = await session.execute(
        select(User).where(User.state == UserState.activo, User.premium == True)
    )
    return result.scalars().all()

# --------- TAREAS ---------
async def create_task(session, task_data):
    task = Task(**task_data.dict())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def list_all_tasks(session):
    result = await session.execute(select(Task))
    return result.scalars().all()

async def list_tasks_by_user(session, user_id: int):
    result = await session.execute(select(Task).where(Task.user_id == user_id))
    return result.scalars().all()

async def update_task_state(session, task_id: int, new_state: TaskState):
    task = await session.get(Task, task_id)
    if task:
        task.state = new_state
        await session.commit()
        await session.refresh(task)
    return task
