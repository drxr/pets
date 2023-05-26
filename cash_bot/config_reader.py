from pydantic import BaseSettings, SecretStr

# настройки бота для токена
class Settings(BaseSettings):
    bot_token: SecretStr
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

config = Settings()
