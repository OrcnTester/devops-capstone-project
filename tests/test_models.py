import os
import unittest

from service import create_app, db
from service.models import Account, DataValidationError

class TestAccountModel(unittest.TestCase):
    def setUp(self):
        os.environ["DATABASE_URI"] = "sqlite://"
        self.app = create_app()
        self.app.config["TESTING"] = True

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_account(self):
        with self.app.app_context():
            account = Account(name="Ada", email="ada@example.com")
            db.session.add(account)
            db.session.commit()
            self.assertIsNotNone(account.id)

    def test_serialize_deserialize(self):
        with self.app.app_context():
            data = {"name": "Grace", "email": "grace@example.com"}
            account = Account().deserialize(data)
            self.assertEqual(account.name, "Grace")
            self.assertEqual(account.email, "grace@example.com")
            self.assertIn("name", account.serialize())

    def test_deserialize_missing_fields(self):
        with self.app.app_context():
            with self.assertRaises(DataValidationError):
                Account().deserialize({"email": "x@y.com"})
