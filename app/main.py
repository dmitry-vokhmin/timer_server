from multiprocessing import Process

import pika
import uvicorn
from fastapi import FastAPI

from app.repository import Base, engine
from app.router.timer import router as timer_router
from app.service import rabbitmq
from app.service.rabbitmq import consumer
from app.service.rabbitmq.consumer import start_consumer

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Timer',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json'
)


@app.on_event('startup')
async def startup():
    queue = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    process = Process(target=start_consumer)
    process.start()
    consumer.process = process
    rabbitmq.queue = queue


@app.on_event('shutdown')
async def shutdown():
    consumer.process.terminate()
    consumer.process.close()


app.include_router(timer_router, prefix='/api', tags=['Timer'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
