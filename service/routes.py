from flask import Blueprint, jsonify, request

from service import db
from service.models import Account, DataValidationError

bp = Blueprint("routes", __name__)


def error(status: int, message: str):
    return jsonify({"error": message}), status


@bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"}), 200


@bp.route("/accounts", methods=["POST"])
def create_account():
    try:
        data = request.get_json(force=True, silent=False)
        account = Account().deserialize(data)
        db.session.add(account)
        db.session.commit()
        return jsonify(account.serialize()), 201
    except DataValidationError as e:
        db.session.rollback()
        return error(400, str(e))
    except Exception as e:
        db.session.rollback()
        return error(400, f"Bad Request: {e}")


@bp.route("/accounts", methods=["GET"])
def list_accounts():
    name = request.args.get("name")
    email = request.args.get("email")

    query = Account.query
    if name:
        query = query.filter(Account.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Account.email.ilike(f"%{email}%"))

    results = [a.serialize() for a in query.order_by(Account.id.asc()).all()]
    return jsonify(results), 200


@bp.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id: int):
    account = Account.query.get(account_id)
    if not account:
        return error(404, f"Account {account_id} not found")
    return jsonify(account.serialize()), 200


@bp.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id: int):
    account = Account.query.get(account_id)
    if not account:
        return error(404, f"Account {account_id} not found")

    try:
        data = request.get_json(force=True, silent=False)
        account.deserialize(data)
        db.session.commit()
        return jsonify(account.serialize()), 200
    except DataValidationError as e:
        db.session.rollback()
        return error(400, str(e))
    except Exception as e:
        db.session.rollback()
        return error(400, f"Bad Request: {e}")


@bp.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id: int):
    account = Account.query.get(account_id)
    if not account:
        return error(404, f"Account {account_id} not found")
    db.session.delete(account)
    db.session.commit()
    return "", 204
