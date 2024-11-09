from injector import Binder, Injector

from running_app.common.cache.cache import CacheManager
from running_app.common.cache.redis import RedisManager
from running_app.common.database.db_context import DBContext
from running_app.common.database.sa_context import (
    AsyncSQLAlchemy,
    AsyncSQLAlchemyContext,
)
from running_app.crew.application.create_crew_usecase import CreateCrewUseCase
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
from running_app.running.run.adapter.output.persistence.run_persistence_adapter import (
    RunPersistenceAdapter,
)
from running_app.running.run.application.input.usecase.create_run_usecase import (
    CreateRunUseCase,
)
from running_app.running.run.application.input.usecase.update_run_usecase import (
    UpdateRunUseCase,
)
from running_app.running.run.application.output.find_run_output import FindRunOutput
from running_app.running.run.application.output.save_run_output import SaveRunOutput
from running_app.running.run.application.run_service import RunService
from running_app.running.running_state.adapter.output.cache.running_state_cache_adapter import (
    RunningStateCacheAdapter,
)
from running_app.running.running_state.adapter.output.persistence.running_state_persistence_adapter import (
    RunningStatePersistenceAdapter,
)
from running_app.running.running_state.application.port.input.create_running_status_usecase import (
    CreateRunningStatusUseCase,
)
from running_app.running.running_state.application.port.output.find_current_run_output import (
    FindCurrentRunOutput,
)
from running_app.running.running_state.application.port.output.save_current_run_output import (
    SaveCurrentRunOutput,
)
from running_app.running.running_state.application.port.output.save_running_state_output import (
    SaveRunningStateOutput,
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
from running_app.crew.application.crew_service import CrewService
from running_app.crew.adapter.crew_repository import CrewRepository
from running_app.crew.application.accept_invite_usecase import AcceptInviteUseCase
from running_app.crew.application.invite_usecase import InviteUseCase
from running_app.crew.application.get_crew_members_usecase import GetCrewMembersUseCase

from injector import singleton


def service_configure(binder: Binder) -> None:  # noqa: PLR0915
    binder.bind(DBContext, to=AsyncSQLAlchemyContext, scope=singleton)

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
    binder.bind(
        SaveRunningStateOutput, to=RunningStatePersistenceAdapter, scope=singleton
    )
    binder.bind(SaveCurrentRunOutput, to=RunningStateCacheAdapter, scope=singleton)
    binder.bind(FindCurrentRunOutput, to=RunningStateCacheAdapter, scope=singleton)

    # run
    binder.bind(CreateRunUseCase, to=RunService, scope=singleton)
    binder.bind(UpdateRunUseCase, to=RunService, scope=singleton)
    binder.bind(SaveRunOutput, to=RunPersistenceAdapter, scope=singleton)
    binder.bind(FindRunOutput, to=RunPersistenceAdapter, scope=singleton)

    binder.bind(CacheManager, to=RedisManager, scope=singleton)
    binder.bind(AsyncSQLAlchemy, to=AsyncSQLAlchemy, scope=singleton)

    # crew
    binder.bind(InviteUseCase, to=CrewService, scope=singleton)
    binder.bind(AcceptInviteUseCase, to=CrewService, scope=singleton)
    binder.bind(GetCrewMembersUseCase, to=CrewService, scope=singleton)
    binder.bind(CrewRepository, to=CrewRepository, scope=singleton)
    binder.bind(CreateCrewUseCase, to=CrewService, scope=singleton)


injector = Injector(modules=[service_configure])
