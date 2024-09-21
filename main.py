# -*- coding: utf-8 -*-
from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from app.core.rabbitmq import RabbitMQHandler
from config import get_settings
import multiprocessing
import threading
import sentry_sdk
from app.routes.auth import router as auth_router
from app.routes.company import router as company_router
from app.routes.users import router as user_router
from app.routes.students import router as student_router
from app.routes.skills import router as skill_router
from app.routes.instructors import router as instuctor_router
from app.routes.schedules import router as schedule_router
from app.routes.notifications import router as notifications_router
from app.routes.executions import router as execution_router
from app.routes.follow_up import router as follow_up_router
from app.routes.profile import router as profile_router
from app.routes.avatar import router as avatar_router
from app.routes.specialties import router as specialty_router
from app.routes.api_requests import router as api_requests_router


# sentry_sdk.init(
#     dsn="https://3ace38572162064e6cc3487a1795249d@o4507711488589824.ingest.us.sentry.io/4507711490818048",
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     traces_sample_rate=1.0,
#     # Set profiles_sample_rate to 1.0 to profile 100%
#     # of sampled transactions.
#     # We recommend adjusting this value in production.
#     profiles_sample_rate=1.0,
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
app.include_router(company_router, prefix='/companies')
app.include_router(user_router, prefix='/users')
app.include_router(instuctor_router, prefix='/instructors')
app.include_router(student_router, prefix='/students')
app.include_router(skill_router, prefix='/skills')
app.include_router(schedule_router, prefix='/schedules')
app.include_router(execution_router, prefix='/execution')
app.include_router(follow_up_router, prefix='/follow-up')
app.include_router(profile_router, prefix='/profile')
app.include_router(avatar_router, prefix='/avatars')
app.include_router(specialty_router, prefix='/specialties')
app.include_router(api_requests_router, prefix='/api-requests')

# routes provisional
app.include_router(notifications_router, prefix='/notifications')

# rabbit = RabbitMQHandler()
# consumer_thread = threading.Thread(target=rabbit.listener).start()

if __name__ == "__main__":
    host_process = multiprocessing.Process(
        target=uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True))
    host_process.start()