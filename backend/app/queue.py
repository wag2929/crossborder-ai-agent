import asyncio
from datetime import datetime
from sqlmodel import Session, select
from app.database import engine
from app.models import Task, TaskStatus
from app.notify import notify_feishu
from app.orchestrator import orchestrator


async def process_task(task_id: int) -> None:
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            return
        task.status = TaskStatus.running.value
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()

    try:
        result = await asyncio.to_thread(orchestrator.run, task.task_type, task.payload)
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if task is None:
                return
            task.status = TaskStatus.completed.value
            task.result = result
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
        await notify_feishu("CrossBorder AI Agent task completed", {"task_id": task_id, "task_type": task.task_type})
    except Exception as exc:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if task is None:
                return
            task.status = TaskStatus.failed.value
            task.error = str(exc)
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
        await notify_feishu("CrossBorder AI Agent task failed", {"task_id": task_id, "error": str(exc)})


async def queue_worker(stop_event: asyncio.Event) -> None:
    while not stop_event.is_set():
        task_id: int | None = None
        with Session(engine) as session:
            statement = select(Task).where(Task.status == TaskStatus.pending.value).order_by(Task.created_at).limit(1)
            task = session.exec(statement).first()
            if task is not None:
                task.status = TaskStatus.running.value
                task.updated_at = datetime.utcnow()
                session.add(task)
                session.commit()
                task_id = task.id

        if task_id is not None:
            await process_task(task_id)
        else:
            await asyncio.sleep(2)
