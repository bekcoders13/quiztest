import inspect
from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from functions.results import add_result_f
from models.finalresult import FinalResults
from models.result import Results
from models.user import Users
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.results import CreateResult
from schemas.user import CreateUser
from db import database


results_router = APIRouter(
    prefix="/results",
    tags=["Yetakchilar, natija qo'shish va ularni ko'rish"]
)


@results_router.get('/get')
async def get_result(db: Session = Depends(database),
                     current_user: CreateUser = Depends(get_current_active_user)):
    await role_verification(current_user, inspect.currentframe().f_code.co_name)
    item = db.query(Results).all()
    return item


@results_router.post('/create')
async def add_result(form: CreateResult, db: Session = Depends(database),
                     current_user: CreateUser = Depends(get_current_active_user)):
    await role_verification(current_user, inspect.currentframe().f_code.co_name)
    await add_result_f(form, db)
    raise HTTPException(200, "Success")


@results_router.get('/get_final_result')
async def get_common_result(db: Session = Depends(database),
                            current_user: CreateUser = Depends(get_current_active_user)):
    await role_verification(current_user, inspect.currentframe().f_code.co_name)
    items = (db.query(FinalResults).
             options(joinedload(FinalResults.user).load_only(Users.firstname, Users.lastname)).all())
    return items
