from dataclasses import dataclass, asdict
from os import path, environ

base_dir = path.dirname(path.abspath(__file__))

#해당 변수들의 불변성을 위해 dataclass의 fronzen 옵션 사용

@dataclass(frozen=True)
class DataBase:
    user: str
    password: str
    host: str
    port: int
    database: str

@dataclass(frozen=True)
class Envs(DataBase):
    jwt_secret_key: str 
    jwt_expire_time: int
    base_dir= base_dir
    proj_reload: bool =False
    app_port: int =5001
    server_name: str ="/paythere/api"

#개발모드별 환경변수 선택을 위한 딕셔너리
env_mods={
    "local":
        Envs(
            user="root",
            password="test_mysql",
            host="localhost",
            port=3000,
            database="paythere",
            jwt_secret_key="jwt_paythere",
            jwt_expire_time=60*60*24*7,
            proj_reload=True,
    ),
    "test":
        Envs(
            user="test",
            password="test_mysql",
            host="localhost",
            port=3001,
            database="paythere_test",
            jwt_secret_key="jwt_paythere",
            jwt_expire_time=60*60*24*7,
            proj_reload=True,
            app_port=5002
        ),
    "pro":
        Envs(
            user="root",
            password="test_mysql",
            host="localhost",
            port=3000,
            database="paythere",
            jwt_secret_key="jwt_paythere",
            jwt_expire_time=60*60*24*7,
    ),
}

def make_conf_dict():
    env_name=environ.get("APP_ENV", "local")
    if env_name not in env_mods:
        env_name="local"
    return env_mods[env_name]