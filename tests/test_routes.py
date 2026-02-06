import os
import unittest
import json

from service import create_app, db


class TestRoutes(unittest.TestCase):
    def setUp(self):
        os.environ["DATABASE_URI"] = "sqlite://"
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _create(self, name="Ada", email="ada@example.com"):
        resp = self.client.post(
            "/accounts",
            data=json.dumps({"name": name, "email": email}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 201)
        return resp.get_json()["id"]

    def test_health(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["status"], "OK")

    def test_crud_flow(self):
        # Create
        aid = self._create()
        # Read
        resp = self.client.get(f"/accounts/{aid}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Ada")

        # Update
        resp = self.client.put(
            f"/accounts/{aid}",
            data=json.dumps({"name": "Ada L.", "email": "ada@example.com"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Ada L.")

        # List
        resp = self.client.get("/accounts")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.get_json()) >= 1)

        # Delete
        resp = self.client.delete(f"/accounts/{aid}")
        self.assertEqual(resp.status_code, 204)

        # Read missing
        resp = self.client.get(f"/accounts/{aid}")
        self.assertEqual(resp.status_code, 404)

    def test_list_filters(self):
        self._create(name="Ada", email="ada@example.com")
        self._create(name="Grace", email="grace@example.com")

        resp = self.client.get("/accounts?name=grace")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), 1)

        resp = self.client.get("/accounts?email=ada@")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), 1)
