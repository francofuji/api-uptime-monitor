from fastapi import FastAPI
from mangum import Mangum
from backend.routers import user

app = FastAPI()
app.include_router(user.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

handler = Mangum(app)
