from __future__ import annotations
from typing import List, Optional

from litestar import Controller, get, post, put, delete
from litestar.exceptions import NotFoundException
from sqlspec.adapters.aiosqlite import AiosqliteDriver


from models import Task, TaskCreate, TaskUpdate


class TaskController(Controller):
    path = "/tasks"
    # dependencies = {"db_session": Provide(get_db_session)}

    @get()
    async def list_tasks(
        self,
        db_session: "AiosqliteDriver",
        completed: Optional[bool] = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[Task]:
        query = "SELECT id, title, description, completed, priority, due_date, created_at, updated_at FROM tasks"
        params = []

        if completed is not None:
            query += " WHERE completed = ?"
            params.append(completed)

        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        res = await db_session.execute(query, *params)
        tasks = res.get_data(schema_type=Task)
        return tasks

    @post()
    async def create_task(
        self,
        data: TaskCreate,
        db_session: "AiosqliteDriver",
    ) -> Task:
        task = await db_session.select_one(
            """
            INSERT INTO tasks (title, description, completed, priority, due_date)
            VALUES (?, ?, ?, ?, ?)
            RETURNING id, title, description, completed, priority, due_date, created_at, updated_at
            """,
            data.title,
            data.description or "",
            data.completed,
            data.priority,
            data.due_date,
            schema_type=Task
        )
        await db_session.commit()
        return task

    @get("/{task_id:int}")
    async def get_task(
        self,
        task_id: int,
        db_session: "AiosqliteDriver",
    ) -> Task:
        task = await db_session.select_one_or_none(
            """
             SELECT id, title, description, completed, priority, due_date, created_at, updated_at
             FROM tasks
             WHERE id = ?
            """,
            task_id,
            schema_type=Task
        )
        if task is None:
            raise NotFoundException(f"Task with ID {task_id} not found")
        return task

    @put("/{task_id:int}")
    async def update_task(
        self,
        task_id: int,
        data: TaskUpdate,
        db_session: "AiosqliteDriver",
    ) -> Task:

        update_fields = []
        params = []

        if data.title is not None:
            update_fields.append("title = ?")
            params.append(data.title)
        if data.description is not None:
            update_fields.append("description = ?")
            params.append(data.description)
        if data.completed is not None:
            update_fields.append("completed = ?")
            params.append(data.completed)
        if data.priority is not None:
            update_fields.append("priority = ?")
            params.append(data.priority)
        if data.due_date is not None:
            update_fields.append("due_date = ?")
            params.append(data.due_date)

        if not update_fields:
            return {}

        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        params.append(task_id)

        query = f"""
            UPDATE tasks
            SET {', '.join(update_fields)}
            WHERE id = ?
            RETURNING id, title, description, completed, priority, due_date, created_at, updated_at
        """

        task = await db_session.select_one(
            query,
            params
        )

        return task

    @delete("/{task_id:int}", status_code=204)
    async def delete_task(
        self,
        task_id: int,
        db_session: "AiosqliteDriver",
    ) -> None:
        result = await db_session.select_one_or_none(
            "DELETE FROM tasks WHERE id = ? RETURNING id",
            task_id
        )
        if result is None:
            raise NotFoundException(f"Task with ID {task_id} not found")
        await db_session.commit()
