import pathlib
from typing import Optional
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import NoResultFound

db = SQLAlchemy()
migrate = Migrate(db=db, directory=pathlib.Path(__file__).parent.joinpath("migrations"))


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String(length=36), primary_key=True)
    account = db.Column(db.String(length=69), nullable=False)
    memo = db.Column(db.Integer)
    email = db.Column(db.String(length=254))
    first_name = db.Column(db.String(length=32))
    last_name = db.Column(db.String(length=32))

    @classmethod
    def get(
        cls,
        id: Optional[str] = None,
        account: Optional[str] = None,
        memo: Optional[int] = None,
        email: Optional[str] = None,
    ) -> "User":
        if not any([id, account, memo, email]):
            raise ValueError("no arguments provided")
        kwargs = {}
        if id:
            kwargs["id"] = id
        if account:
            kwargs["account"] = account
        if memo:
            kwargs["memo"] = memo
        if email:
            kwargs["email"] = email
        return db.session.query(User).filter_by(**kwargs).one()

    @classmethod
    def get_or_create(
        cls,
        id: Optional[str] = None,
        account: Optional[str] = None,
        memo: Optional[int] = None,
        email: Optional[str] = None,
    ) -> "User":
        try:
            user = cls.get(id=id, account=account, memo=memo, email=email)
        except NoResultFound:
            user = User(
                id=id if id else str(uuid4()), account=account, memo=memo, email=email
            )
            db.session.add(user)
        return user


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.String(length=36), primary_key=True)
    user_id = db.Column(db.String(length=256), db.ForeignKey("user.id"))
    ref_num = db.Column(db.Integer)

    user = db.orm.relationship("User")
