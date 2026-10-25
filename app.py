from fastapi import FastAPI


APP_VERSION = "0.1.0"

app = FastAPI(
    title="to-do list",
    description="Cервис для учёта задач",
    version=APP_VERSION,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/version")
def version() -> dict[str, str]:
    return {"version": APP_VERSION}