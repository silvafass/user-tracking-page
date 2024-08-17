# User Tracking Page application - A Development Testing Task

## Develpment setup
Create venv and install dependencies only for convenience of local development along with text editor, it is not mandatory to run the project.
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
pip install --upgrade -r requirements-dev.txt
```

### Run pre-commit hooks manually
Eventually, you may want to run pre-commit hooks to perform a general check of the codebase, as well as to maintain good code formatting.
```bash
pre-commit run --all-files
```

## Run application via docker compose
Run docker compose and access the web page at http://localhost
```bash
docker compose up --build
```
To clean the container and volumes:
```bash
docker compose down -v
```
