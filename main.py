from fastapi import FastAPI

import uvicorn

from api.router import router

app = FastAPI()

app.include_router(router)


@app.get("/check_site")
def check_site_work():
    return "Hello World!"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, reload_dirs=["."], port=7997)
