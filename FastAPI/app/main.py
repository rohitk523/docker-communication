from fastapi import FastAPI

from . import db_database, models
from .routers import txt_upload, user

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


models.Base.metadata.create_all(bind=db_database.engine)

app.include_router(user.router)
app.include_router(txt_upload.router)


# current_user: schemas.User = Depends(get_current_user)
