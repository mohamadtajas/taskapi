from itertools import count

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Task API", version="0.1.0")


class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    done: bool = False


class Task(TaskIn):
    id: int


_tasks: dict[int, Task] = {}
_ids = count(1)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return list(_tasks.values())


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskIn) -> Task:
    task = Task(id=next(_ids), **payload.model_dump())
    _tasks[task.id] = task
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return _tasks[task_id]
