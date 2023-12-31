from environs import Env
from dataclasses import dataclass

@dataclass
class Config:
    BOT_TOKEN: str
    ADMIN_ID: int
    PSQL_URL: str
    API_KEY: str

def get_config(path):
    env = Env()
    env.read_env(path)
    return Config(env.str("TOKEN"), env.int("ADMIN_ID"), env.str('PSQL_URL'), env.str('API_KEY'))