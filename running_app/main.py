from running_app.user.adapter.input.web.user_controller import user_router
from running_app.path.adapter.input.web.path_controller import path_router
from running_app.running.run.adapter.input.web.run_controller import run_router
from running_app.running.running_state.adapter.input.web.running_state_controller import (
    running_state_router,
)
from fastapi import FastAPI


app = FastAPI()


app.include_router(user_router)
app.include_router(path_router)
app.include_router(run_router)
app.include_router(running_state_router)
