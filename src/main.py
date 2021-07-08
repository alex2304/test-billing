from fastapi import FastAPI

from handlers import router

app = FastAPI(routes=[router])
