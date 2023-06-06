from environs import Env
env = Env()
env.read_env(".env")
TOKEN = env.str("TOKEN")
weather_API = env.str("weather_API")