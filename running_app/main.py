from running_app.user.adapter.input.web.user_controller import user_router
from running_app.path.adapter.input.web.path_controller import path_router

from fastapi import FastAPI


app = FastAPI()


app.include_router(user_router)
app.include_router(path_router)
