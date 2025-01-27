# Library Example Project
The purpose of this project appears to be a library management system,
which allows users to create, read, update, and delete patrons and books. The system also includes features such as asynchronous task processing using Celery and database migration management using Alembic.


## Running the app using docker

Setup env variables in `app/core/.env` (please change it to your own values).
```bash
RELOAD=True
DB_HOST=your_db_host
DB_PORT=5432
DB_USER=your_db_user
DB_PASS=your_db_pass
DB_BASE=your_db_name
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


## Running the project without docker

#### Create  and activate venv (For Linux)

```bash
python -m venv myenv

source myenv/bin/activate 

```
#### Install dependencies

```bash
cd app/
pip install -r requirements.txt
```

Setup env variables in `app/core/.env`.


Apply migrations

```bash
cd app/
alembic upgrade head
```


#### Run server

```bash
cd app/
python app/server.py
```
Go to: http://localhost:8000/api/docs/

#### Run celery for periodic tasks and beat
Open a new terminal
```bash
cd app/
celery -A tasks.library_tasks worker --beat --loglevel=info
```

#### Extra
* Please make sure you have postgresql, mailhog and redis installed on your machine if you are not working with docker .
* As python 3.10.0 is being used with docker this version is suggested to be installed on your machine.
* please take a look at screenshots under docker folder for better experience
