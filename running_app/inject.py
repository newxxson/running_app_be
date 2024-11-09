from injector import Binder, Injector

from running_app.common.database.db_context import DBContext
from running_app.common.database.sa_context import AsyncSQLAlchemyContext
from running_app.path.adapter.output.persistence.path_persistence_adapter import (
    PathPersistenceAdapter,
)
from running_app.path.application.input.usecase.create_path_usecase import (
    CreatePathUseCase,
)
from running_app.path.application.input.usecase.query_path_usecase import (
    QueryPathUseCase,
)
from running_app.path.application.input.usecase.register_coordinate_usecase import (
    RegisterCoordinateUseCase,
)
from running_app.path.application.output.query_path_output import QueryPathOutput
from running_app.path.application.output.save_coordinate_output import (
    SaveCoordinateOutput,
)
from running_app.path.application.output.save_path_output import SavePathOutput
from running_app.path.application.path_service import PathService
from running_app.running.running_state.application.port.input.create_running_status_usecase import (
    CreateRunningStatusUseCase,
)
from running_app.running.running_state.application.running_state_service import (
    RunningStateService,
)
from running_app.user.adapter.output.persistence.user_persistence_adapter import (
    UserPersistenceAdapter,
)
from running_app.user.adapter.output.web.kakao_request import KakaoApiRequest
from running_app.user.application.port.input.create_user_usecase import (
    CreateUserUseCase,
)
from running_app.user.application.port.input.login_user_usecase import LoginUserUseCase
from running_app.user.application.port.input.query_user_usecase import QueryUserUseCase
from running_app.user.application.port.output.find_user_output import FindUserOutput
from running_app.user.application.port.output.get_user_info_output import (
    GetUserInfoOutput,
)
from running_app.user.application.port.output.save_user_output import SaveUserOutput
from running_app.user.application.user_service import UserService
from injector import singleton


def service_configure(binder: Binder) -> None:  # noqa: PLR0915
    binder.bind(DBContext, to=AsyncSQLAlchemyContext)

    # user
    binder.bind(GetUserInfoOutput, to=KakaoApiRequest, scope=singleton)
    binder.bind(FindUserOutput, to=UserPersistenceAdapter, scope=singleton)
    binder.bind(SaveUserOutput, to=UserPersistenceAdapter, scope=singleton)
    binder.bind(CreateUserUseCase, to=UserService, scope=singleton)
    binder.bind(QueryUserUseCase, to=UserService, scope=singleton)
    binder.bind(LoginUserUseCase, to=UserService, scope=singleton)
    binder.bind(GetUserInfoOutput, to=KakaoApiRequest, scope=singleton)

    # path
    binder.bind(CreatePathUseCase, to=PathService, scope=singleton)
    binder.bind(QueryPathUseCase, to=PathService, scope=singleton)
    binder.bind(RegisterCoordinateUseCase, to=PathService, scope=singleton)
    binder.bind(QueryPathOutput, to=PathPersistenceAdapter, scope=singleton)
    binder.bind(SavePathOutput, to=PathPersistenceAdapter, scope=singleton)
    binder.bind(SaveCoordinateOutput, to=PathPersistenceAdapter, scope=singleton)

    # running state
    binder.bind(CreateRunningStatusUseCase, to=RunningStateService, scope=singleton)


injector = Injector(modules=[service_configure])
