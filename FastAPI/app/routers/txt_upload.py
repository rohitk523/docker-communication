import shutil
from datetime import datetime

import requests  # type: ignore
from requests import Session

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Security,
    UploadFile,
    status,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .. import models
from ..auth import Auth
from ..db_database import get_db
from ..word_count import keywords_word_count, list_keywords, txt_len, word_count

auth_handler = Auth()
security = HTTPBearer()

router = APIRouter(prefix="", tags=["Upload"])


@router.post("/keywords")
def upload_keywords_file(
    file: UploadFile = File(),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    if file.filename[-3:] != "csv":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="File uploaded is not a .csv file \n Please upload .csv file",
        )
    else:
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        token = credentials.credentials
        decoded = auth_handler.decode_token(token)
        user = (
            db.query(models.User)
            .filter(models.User.username == decoded)
            .first()
        )
        if decoded == user.username:
            file_details = models.keywords(
                filename=file.filename,
                list_keywords=list_keywords(file.filename),
                user_id=user.uuid,
            )
            all_files = []
            for i in (
                db.query(models.keywords)
                .filter(models.keywords.user_id == file_details.user_id)
                .all()
            ):
                all_files.append(i.filename)
            if file_details.filename in all_files:
                return HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="file already exists",
                    headers="File management",
                )
            else:
                if (
                    db.query(models.keywords)
                    .filter(models.keywords.user_id == user.uuid)
                    .count()
                    == 1
                ):
                    db.query(models.keywords).filter(
                        models.keywords.user_id == user.uuid
                    ).delete()
                    db.add(file_details)
                    db.commit()
                    db.refresh(file_details)
                    return f"You have replaced keywords file with {file_details.filename}"
                else:
                    db.add(file_details)
                    db.commit()
                    db.refresh(file_details)
                    return "KEYWORDS UPLOADED SUCCESSFULLY"
        else:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )


@router.post("/Word Count")
def upload_text_file(
    file: UploadFile = File(),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    if file.filename[-3:] != "txt":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="File uploaded is not a text file \n Please upload text file",
        )
    else:
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        token = credentials.credentials
        decoded = auth_handler.decode_token(token)
        user = (
            db.query(models.User)
            .filter(models.User.username == decoded)
            .first()
        )
        if decoded == user.username:
            file_details = models.file_data(
                filename=file.filename,
                length=txt_len(file.filename),
                user_id=user.uuid,
            )

            keyword_file = (
                db.query(models.keywords)
                .filter(models.keywords.user_id == user.uuid)
                .first()
            )

            all_files = []
            for i in (
                db.query(models.file_data)
                .filter(models.file_data.user_id == file_details.user_id)
                .all()
            ):
                all_files.append(i.filename)
            if file_details.filename in all_files:
                return HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="file name already exists",
                    headers="File management",
                )
            for i in range(len(all_files)):
                if (
                    open(file_details.filename, encoding="utf-8").read()
                    == open(all_files[i], encoding="utf-8").read()
                ):
                    return HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="same file data already exists",
                        headers="File management",
                    )
            else:
                db.add(file_details)
                db.commit()
                db.refresh(file_details)
                if (
                    db.query(models.keywords)
                    .filter(models.keywords.user_id == user.uuid)
                    .count()
                    == 0
                ):
                    wordcount = word_count(file.filename)
                    total = sum(list(wordcount.values()))
                else:
                    wordcount = keywords_word_count(
                        file.filename, keyword_file.filename
                    )
                    total = sum(list(wordcount.values()))

            x = requests.post(
                "http://textfile:8086/requests",
                json={
                    "name": user.username,
                    "filename": file_details.filename,
                    "time": str(datetime.now().strftime("%c")),
                    "wordcount": total,
                },
            )
            print(x.text)
            return wordcount
        else:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )


@router.get("/Get User stats")
def all(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    token = credentials.credentials
    decoded = auth_handler.decode_token(token)
    user = db.query(models.User).filter(models.User.username == decoded).first()
    keyword_file = (
        db.query(models.keywords)
        .filter(models.keywords.user_id == user.uuid)
        .first()
    )
    file_details = (
        db.query(models.file_data)
        .filter(models.file_data.user_id == user.uuid)
        .all()
    )
    count1 = 0
    count2 = 0
    for i in range(len(file_details)):
        wordcount = word_count(file_details[i].filename)
        count1 += sum(list(wordcount.values()))

    for i in range(len(file_details)):
        wordcount = keywords_word_count(
            file_details[i].filename, keyword_file.filename
        )
        count2 += sum(list(wordcount.values()))

    return {
        "user id": user.uuid,
        "total files uploaded": len(file_details),
        "word count with keywords": count2,
        "word count with no keywords": count1,
        "Overall word count": count1 + count2,
    }
