import os

from pydantic_settings import BaseSettings, SettingsConfigDict

setting_profiles = ("local", "dev", "stg", "prod")
profile = os.getenv("PROFILE")
if not profile or profile not in setting_profiles:
    message = f"PROFILE 이 설정되지 않았습니다. PROFILE 환경변수를 설정해주세요, PROFILE={profile}."
    raise ValueError(message)


class BaseProperty(BaseSettings):
    """PROFILE 값에 따라 다른 파일을 통해 각 property들이 상속받는 기본 Property 형식입니다."""

    model_config = SettingsConfigDict(env_file=(".env/.env", f".env/.env-{profile}"), extra="ignore")

    profile: str
    