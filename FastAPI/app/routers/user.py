import uuid

from requests import Session

from fastapi import APIRouter, Depends, HTTPException, status

from .. import models, schemas
from ..auth import Auth
from ..db_database import get_db

router = APIRouter(prefix="/user", tags=["User"])

auth_handler = Auth()


@router.post("/")
def create_User(request: schemas.User, db: Session = Depends(get_db)):
    new_uuid = str(uuid.uuid4())
    new_user = models.User(username=request.username, uuid=new_uuid)
    all_users = []
    for i in db.query(models.User).all():
        all_users.append(i.username)
    if new_user.username in all_users:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user already exists",
            headers="User management",
        )
    else:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        access_token = auth_handler.encode_token(new_user.username)
        return {"access token": access_token, "uuid": new_uuid}


@router.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0
    return division_by_zero
