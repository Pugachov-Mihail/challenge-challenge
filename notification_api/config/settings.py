from envparse import Env

env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default="mongodb+srv://admin:1234@localhost:27017/notification"
)
