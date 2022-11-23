import json
import pathlib

from flask import Flask, render_template, redirect, url_for, request, session
from dotenv import load_dotenv, find_dotenv
from app.auth import verify_jwt
from jwt.exceptions import InvalidTokenError

from app.db import db, migrate, User, Transaction
from app.platform import AnchorPlatformClient

load_dotenv(find_dotenv())

app = Flask(__name__, instance_path=pathlib.Path(__file__).parent.resolve())
app.config.from_prefixed_env()
db.init_app(app)
migrate.init_app(app)


@app.route("/login")
def login():
    try:
        contents = verify_jwt(request.args.get("token"))
    except (ValueError, InvalidTokenError) as e:
        return render_template("error.html", message=str(e)), 401

    with AnchorPlatformClient() as client:
        transaction_json = client.get_transaction(contents["jti"])

    user = User.get_or_create(
        account=transaction_json["customers"]["sender"]["account"],
        memo=transaction_json["customers"]["sender"].get("memo"),
    )
    if not session.get("user_id"):
        session["user_id"] = user.id
    transaction = Transaction(
        id=contents["jti"],
        user_id=user.id,
    )
    db.session.add(transaction)
    db.session.commit()

    session["transaction_id"] = transaction.id
    return redirect(url_for("index"))


@app.route("/")
def index():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    user = User.get(id=session["user_id"])
    short_account = "...".join(["G", user.account[-3:]])
    return render_template("index.html", name=short_account)


@app.route("/logout")
def logout():
    session.clear()
    return render_template("logged_out.html")
