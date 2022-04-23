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

from routes.company import router as company_router
from routes.users import router as user_router


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
              description='Api de comunicação')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(company_router, prefix='/company')
app.include_router(user_router, prefix='/users')



if __name__ == "__main__":
    host_process = multiprocessing.Process(
        target=uvicorn.run(app, host="0.0.0.0", port=settings.PORT))
    host_process.start()
