import inspect
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from functions.questions import get_question_f, create_question_f, update_question_f, delete_question_f
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.questions import CreateQuestion, UpdateQuestion
from schemas.users import CreateUser
from db import database


questions_router = APIRouter(
    prefix="/questions",
    tags=["Questions operation"]
)


@questions_router.get('/get')
def get_question(level: str = None, ident: int = 0, science_id: int = 0,
                 page: int = 1, limit: int = 25,
                 db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_question_f(ident, science_id, level, page, limit, db)


@questions_router.post('/create')
def create(forms: List[CreateQuestion], db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_question_f(forms, db)
    raise HTTPException(status_code=200, detail="Create Success !!!")


@questions_router.put("/update")
def update(form: UpdateQuestion, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_question_f(form, db)
    raise HTTPException(status_code=200, detail="Update Success !!!")


@questions_router.delete("/delete")
def delete(ident: int = 0, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_question_f(ident, db)
    raise HTTPException(status_code=200, detail="Delete Success !!!")


