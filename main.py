from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from api import test, get, post
import uvicorn
import config

app = FastAPI(debug=config.uvicorn_debug, docs_url='/api/docs', openapi_url='/api/openapi.json', redoc_url='/api/redoc')
register_tortoise(app, db_url=config.mysqlurl, modules={"models": ["libs.models"]},
                  add_exception_handlers=config.uvicorn_debug)
app.include_router(router=test.router)
app.include_router(router=get.router)
app.include_router(router=post.router)

if __name__ == "__main__":
    uvicorn.run(app='main:app', host=config.uvicorn_host, port=config.uvicorn_port, reload=config.uvicorn_reload,
                workers=2)
