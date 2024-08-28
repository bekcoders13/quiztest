from routes.login import get_password_hash
from utils.db_operations import save_in_db
from utils.pagination import pagination
from models.users import Users


def get_user_f(ident, search, page, limit, role, db):

    if ident > 0:
        ident_filter = Users.id == ident
    else:
        ident_filter = Users.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Users.region.like(search_formatted) |
                         Users.username.like(search_formatted))
    else:
        search_filter = Users.id > 0

    if role == "boss":
        role_filter = Users.role == "boss"
    elif role == "admin":
        role_filter = Users.role == "admin"
    else:
        role_filter = Users.id > 0

    items = db.query(Users).filter(ident_filter, search_filter, role_filter).order_by(Users.id.desc())

    return pagination(items, page, limit)


def create_user_f(form, db):
    new_item_db = Users(
        firstname=form.firstname,
        lastname=form.lastname,
        username=form.username,
        gender=form.gender,
        region=form.region,
        town=form.town,
        birthdate=form.birthdate,
        role="admin",
        password=get_password_hash(form.password))
    save_in_db(db, new_item_db)


def create_general_user_f(form, db):
    new_item_db = Users(
        firstname=form.firstname,
        lastname=form.lastname,
        username=form.username,
        gender=form.gender,
        region=form.region,
        town=form.town,
        birthdate=form.birthdate,
        role="user",
        password=get_password_hash(form.password))
    save_in_db(db, new_item_db)


def update_user_f(form, db, user):
    db.query(Users).filter(Users.id == user.id).update({
        Users.firstname: form.firstname,
        Users.lastname: form.lastname,
        Users.gender: form.gender,
        Users.birthdate: form.birthdate,
        Users.region: form.region,
        Users.town: form.town,
        Users.password: get_password_hash(form.password),
        Users.role: user.role,
    })
    db.commit()


def delete_user_f(db, user):
    db.query(Users).filter(Users.id == user.id).delete()
    db.commit()
