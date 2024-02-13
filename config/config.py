from pydantic import Field, AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    amqp_dsn: str = Field(alias='amqp_dsn')
    queue_name: str = Field(alias='queue_name')
    routing_key: str = Field(alias='routing_key')
    dead_queue_name: str = Field(alias='dead_queue_name')
    dead_exchange: str = Field(alias='dead_exchange')
    dead_routing_key: str = Field(alias='dead_routing_key')
    message_ttl: int = Field(alias='message_ttl')


settings = Settings()
