from fastapi import FastAPI
from itertools import count

from fastapi import FastAPI
from pydantic import BaseModel, Field

APP_VERSION = "0.1.0"

app = FastAPI(
    title="to-do list",
    description="Cервис для учёта задач",
    version=APP_VERSION,
)

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class Task(BaseModel):
    id: int
    title: str
    done: bool = False

tasks: dict[int, Task] = {}
task_ids = count(1)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/version")
def version() -> dict[str, str]:
    return {"version": APP_VERSION}

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_data: TaskCreate) -> Task:
    task = Task(
        id=next(task_ids),
        title=task_data.title,
    )

    tasks[task.id] = task

    return task

@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return list(tasks.values())