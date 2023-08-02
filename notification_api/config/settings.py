from envparse import Env

env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default="mongodb://root:1234@localhost:27017/"
)
