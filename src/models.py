from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="タスクのタイトル",
        examples=["買い物に行く"]
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="タスクの詳細説明",
        examples=["牛乳と卵を買う"]
    )
    completed: bool = Field(
        False,
        description="タスクの完了状態",
        examples=[False]
    )
    priority: Priority = Field(
        Priority.MEDIUM,
        description="タスクの優先度",
        examples=["medium"]
    )
    due_date: Optional[datetime] = Field(
        None,
        description="タスクの期限",
        examples=["2023-12-31T23:59:59"]
    )

    @field_validator('title')
    def title_must_contain_letters(cls, v):
        if not any(c.isalpha() for c in v):
            raise ValueError('タイトルには文字が含まれている必要があります')
        return v.strip()


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="タスクのタイトル"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="タスクの詳細説明"
    )
    completed: Optional[bool] = Field(
        None,
        description="タスクの完了状態"
    )
    priority: Optional[Priority] = Field(
        None,
        description="タスクの優先度"
    )
    due_date: Optional[datetime] = Field(
        None,
        description="タスクの期限"
    )


class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "買い物に行く",
                "description": "牛乳と卵を買う",
                "completed": False,
                "priority": "medium",
                "due_date": "2023-12-31T23:59:59",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }
