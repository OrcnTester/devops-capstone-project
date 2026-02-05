# devops-capstone-project

![CI](https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>/actions/workflows/ci-build.yaml/badge.svg)

A small RESTful microservice for managing **Customer Accounts** (CRUD) built with **Flask + SQLAlchemy**.

> Note: This repo uses **nosetests (nose)** for the course rubric, which is most reliable on **Python 3.9**.

## Endpoints

- `POST /accounts` — create an account
- `GET /accounts` — list accounts (supports `?name=` and/or `?email=` filters)
- `GET /accounts/<id>` — read an account
- `PUT /accounts/<id>` — update an account
- `DELETE /accounts/<id>` — delete an account
- `GET /health` — service health check

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
flask --app wsgi:app --debug run -p 8080
```

## Run tests + lint

```bash
flake8 .
nosetests -v
```

## Quick REST smoke test (curl)

```bash
# create
curl -i -X POST http://localhost:8080/accounts \
  -H "Content-Type: application/json" \
  -d '{"name":"Ada Lovelace","email":"ada@example.com"}'

# list
curl -i http://localhost:8080/accounts

# read (replace 1)
curl -i http://localhost:8080/accounts/1

# update (replace 1)
curl -i -X PUT http://localhost:8080/accounts/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Ada L.","email":"ada@example.com"}'

# delete (replace 1)
curl -i -X DELETE http://localhost:8080/accounts/1
```

## Docker

```bash
docker build -t accounts:latest .
docker run --rm -p 8080:8080 accounts:latest
```

## Kubernetes (sample manifests)

See `k8s/` for sample Deployment/Service.
