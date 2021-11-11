from envparse import Env

env = Env()
env.read_envfile()

REDIS_URL = env("REDIS_URL", default="redis.pythonweekend.skypicker.com")
DATABASE_URL = env("DATABASE_URL",
                   default="postgresql://pythonweekend:QA1rWe0HcGo4sNrf@sql.pythonweekend.skypicker.com/pythonweekend")
