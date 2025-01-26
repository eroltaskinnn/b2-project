# Library Example Project

[//]: # (Project includes:)

[//]: # ()
[//]: # (-   `fastapi`)

[//]: # (-   `sqlmodel`)

[//]: # (-   `alembic`)

[//]: # (##)

[//]: # (## Models)

[//]: # ()
[//]: # (Check db/models and migrations, there is one example.)

## Running the app using docker

Setup env variables in `app/core/.env` (plese change it to your own values).
```bash
RELOAD=True
DB_HOST=postgres
DB_PORT=5432
DB_USER=admin
DB_PASS=admin
DB_BASE=test2
MAIL_SERVER=mailhog
MAIL_SERVER_PORT=1025
CELERY_BACKEND_URL=redis://redis:6379
BASE_URL=http://localhost:8000

```


#### Install and run

```bash
docker-compose up -d

# you can track logs with:
docker-compose logs -f --tail=100 web
```

Go to: http://localhost:8000/api/docs/ for swagger


#### Tests

Run tests

```bash
docker-compose exec web pytest .
```

## Running the project without docker

#### Install

```bash
cd app/
pip install -r requirements.txt
```

Setup env variables in `app/core/.env`.

#### Run

```bash
cd app/
python app/server.py
```

Go to: http://localhost:8000/api/docs/



Apply migrations

```bash
alembic upgrade head
```

#### Tests

Run tests

```bash
pytest .
```
