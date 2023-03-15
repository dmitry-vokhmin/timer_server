import uvicorn
from fastapi import FastAPI

from app.repository import Base, engine
from app.router.timer import router as timer_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Timer',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json'
)

app.include_router(timer_router, prefix='/api', tags=['Timer'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
