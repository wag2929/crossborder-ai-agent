from datetime import datetime
from enum import Enum
from typing import Any
from sqlmodel import Field, SQLModel, JSON, Column


class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class TaskType(str, Enum):
    listing = "listing"
    keywords = "keywords"
    localization = "localization"
    customer_service = "customer_service"
    competitor = "competitor"
    product_selection = "product_selection"
    full_workflow = "full_workflow"


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task_type: str = Field(index=True)
    status: str = Field(default=TaskStatus.pending.value, index=True)
    payload: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    result: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON))
    error: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(SQLModel):
    task_type: TaskType
    payload: dict[str, Any]


class TaskRead(SQLModel):
    id: int
    task_type: str
    status: str
    payload: dict[str, Any]
    result: dict[str, Any] | None
    error: str | None
    created_at: datetime
    updated_at: datetime
