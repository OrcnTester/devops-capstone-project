from datetime import datetime

from service import db


class DataValidationError(ValueError):
    """Used for data validation errors when deserializing"""


class Account(db.Model):
    """Model for a customer account"""

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False, index=True)
    address = db.Column(db.String(256), nullable=True)
    phone = db.Column(db.String(32), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def deserialize(self, data: dict):
        if not isinstance(data, dict):
            raise DataValidationError("Invalid account: body must be a JSON object")

        name = data.get("name")
        email = data.get("email")

        if not name or not isinstance(name, str):
            raise DataValidationError("Invalid account: 'name' is required and must be a string")
        if not email or not isinstance(email, str):
            raise DataValidationError("Invalid account: 'email' is required and must be a string")

        self.name = name.strip()
        self.email = email.strip()
        self.address = data.get("address")
        self.phone = data.get("phone")
        return self

    def __repr__(self):
        return f"<Account id={self.id} name={self.name!r} email={self.email!r}>"
