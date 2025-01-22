from fastapi import FastAPI

app = FastAPI()


@app.get("/", summary="Root endpoint")
async def index():
    return {"message": "Root of service"}
