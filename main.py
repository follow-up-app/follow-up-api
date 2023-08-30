# -*- coding: utf-8 -*-
from logging import FATAL, info
from xml.etree.ElementInclude import include
from fastapi_utils.tasks import repeat_every
from fastapi import FastAPI, Depends, BackgroundTasks, background
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from config import get_settings
from dotenv import load_dotenv
from db.seeders.seeders import Seeders
from threading import Thread
from time import sleep
from sqlalchemy.orm.session import Session
from db import get_db
from config import get_settings
import pypeln as pl
from fastapi import BackgroundTasks, FastAPI
from multiprocessing import Process, Event
import multiprocessing
import sentry_sdk
from routes.auth import router as auth_router
from routes.company import router as company_router
from routes.users import router as user_router
from routes.students import router as student_router
from routes.skills import router as skill_router
from routes.procedures import router as procedure_router
from routes.results import router as result_router
from routes.configurations import router as configuration_router
from routes.instructors import router as instuctor_router
from routes.schedule import router as schedule_router



# sentry_sdk.init(
#    "https://9d28606c6ee84d6c87ed3e44be9ef297@o1155311.ingest.sentry.io/6235706",

#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     traces_sample_rate=0.25
# )

origins = [
    "*"
]

settings = get_settings()

app = FastAPI(debug=True, title=settings.APP_NAME,
              description='Api Follow-up')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix='/auth')
app.include_router(company_router, prefix='/company')
app.include_router(user_router, prefix='/users')
app.include_router(instuctor_router, prefix='/instructors')
app.include_router(student_router, prefix='/students')
app.include_router(skill_router, prefix='/skills')
app.include_router(procedure_router, prefix='/procedures')
app.include_router(schedule_router, prefix='/schedules')
app.include_router(result_router, prefix='/results')
app.include_router(configuration_router, prefix='/configurations')



if __name__ == "__main__":
    host_process = multiprocessing.Process(
        target=uvicorn.run(app, host="0.0.0.0", port=settings.PORT))
    host_process.start()
