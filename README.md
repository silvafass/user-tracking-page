# User Tracking Page application
A Development Testing Task

## Run application via docker compose
Run docker compose and access the web page at http://localhost
```bash
docker compose up --build
```
To clean the container and volumes:
```bash
docker compose down -v
```
And acess the web pages:
* http://localhost (The initial page)
* http://localhost/tracking_report (The report page)

Or access the interative API Doc pages:
* http://localhost/docs
* http://localhost/redoc



## Develpment setup
Create venv and install dependencies only for convenience of local development along with text editor, it is not mandatory to run the project.
> [!NOTE]
> This project uses pre-commit, so you will need to run the commands below if you are planning to make commits to the git repository.
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
