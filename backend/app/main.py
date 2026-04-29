import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from app.config import get_settings
from app.database import create_db_and_tables, get_session
from app.models import Task, TaskCreate, TaskRead
from app.queue import queue_worker

stop_event = asyncio.Event()
worker_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global worker_task
    create_db_and_tables()
    stop_event.clear()
    worker_task = asyncio.create_task(queue_worker(stop_event))
    yield
    stop_event.set()
    if worker_task:
        await worker_task


settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "CrossBorder AI Agent API is running"}


@app.post("/api/tasks", response_model=TaskRead)
def create_task(data: TaskCreate, session: Session = Depends(get_session)) -> Task:
    task = Task(task_type=data.task_type.value, payload=data.payload)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/api/tasks", response_model=list[TaskRead])
def list_tasks(session: Session = Depends(get_session)) -> list[Task]:
    statement = select(Task).order_by(Task.created_at.desc()).limit(100)
    return list(session.exec(statement).all())


@app.get("/api/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)) -> Task:
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "time": datetime.utcnow().isoformat()}
