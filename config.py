from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class BotSettings(BaseModel):
    token: str
    skip_updates: bool
    username: str
    admins: list[int]


class DatabaseSettings(BaseModel):
    master_host: str
    slave_host: str
    user: str
    password: str
    database: str
    debug: bool

    @property
    def master_database_url(self):
        return f"mysql+aiomysql://{self.user}:{self.password}@{self.master_host}/{self.database}"

    @property
    def slave_database_url(self):
        return f"mysql+aiomysql://{self.user}:{self.password}@{self.slave_host}/{self.database}"


class RedisSettings(BaseModel):
    host: str
    state: int
    cache: int
    jobs: int


class Config(BaseSettings):
    bot: BotSettings
    database: DatabaseSettings
    redis: RedisSettings

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")


config = Config()  # noqa
