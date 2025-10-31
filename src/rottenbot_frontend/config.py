from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LOGIN_ENDPOINT: str
    SIGNUP_ENDPOINT: str
    PREDICT_ENDPOINT: str
    LOGOUT_ENDPOINT: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# make it usable throughout the app
Config = Settings()
