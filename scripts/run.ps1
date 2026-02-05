python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
$env:FLASK_APP="wsgi:app"
flask --debug run -p 8080
