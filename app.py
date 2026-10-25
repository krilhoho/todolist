from fastapi import FastAPI
from itertools import count

from fastapi import FastAPI, HTTPException
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

def find_task(task_id: int) -> Task:
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Задача не найдена",
        )

    return task

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

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    return find_task(task_id)

@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int) -> Task:
    task = find_task(task_id)
    task.done = True

    return task