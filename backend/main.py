import uvicorn
from fastapi import FastAPI

from app.db.database import Base, engine
from app.models import Employee, EmployeeEvent, TurnoverScore

app = FastAPI(title="Turnover Dashboard API")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
