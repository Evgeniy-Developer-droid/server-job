# Internal-adquanto-backend
## Overview
Master server to manage workers servers
### Admin dashboard
url - /admin/


### Points

---
####`/api/v1/analisys-domain`
method - POST
```json
{
  "url": "google.com",  
  "client": {
    "ip": "192.12.12.12",
    "useragent": "Mozila/5.0 (Macintosh; intel Mac OS X 10_4_5)"
  }
}
```
Results
1. If domain has cache last week - server return them
2. If not has any worker servers - `{'message': "Don't have any slave servers", "type": "error"}` code 502
3. If worker server has some problem - `{"message": "Something was wrong with slave server", "type": "error"}` code 502
4. Job has been added - `{"job": {"id": 342,
   "token": fn4inn4jn3nlkns9s9d2}, "queue": 23}` code 200
---
####`/callback/<int:pk>`
Worker server send result tests on this url

method - POST
```json
{
    "job": {
        "id": "23213",
        "url": "www.daniliants.com",
        "creation_date": "1640358505",
        "processing_time": 22
    },
    "results": {
        "seo": {
          "task1": "result_value"
        },
        "performance": {
          "task1": "result_value",
          "task2": "result_value"
        },
        "other_task_group": {
          "task1": "result_value",
          "task2": "result_value",
          "task3": "result_value"
        }
    }
}
```
Results
1. If everything okay - `{'message': 'OK', 'type': 'success'}` code 200
2. If not authorization request - `{'message': 'Access denied', 'type': 'error'}` code 400
---
####`/report/<int:id>/<str:token>`
Get results from master server

Method - GET

id - job's id

token - job's token

Results
1. Success 
```json
{
    "job": {
        "id": "23213",
        "url": "www.daniliants.com",
        "creation_date": "1640358505",
        "processing_time": 22
    },
    "results": {
        "seo": {
          "task1": "result_value"
        },
        "performance": {
          "task1": "result_value",
          "task2": "result_value"
        },
        "other_task_group": {
          "task1": "result_value",
          "task2": "result_value",
          "task3": "result_value"
        }
    }
}
```
2. If job haven't done - `{"message": "Job haven't done", "type": "warning"}` code 204
3. if job not funded - `{'message': "Job not founded!", 'type': "error"}` code 204
---
## Development
1. Clone this repository on working directory. 
2. Install `Docker` and `docker-compose`.
3. Change files `.env.dev` and `docker-compose.yml` your credentials.
   - Database accesses (optional)
   - Another constants (optional)
4. Building `sudo docker-compose build`
5. Run server `sudo docker-compose up`
6. Create migrations:
   - `sudo docker-compose exec web python manage.py makemigrations`
   - `sudo docker-compose exec web python manage.py migrate`

Creating superuser:
- `sudo docker-compose exec web python manage.py createsuperuser`

Check localhost - 0.0.0.0:8000

If you want to run server like demon mode - use command `sudo docker-compose up -d`

If you change files - you need rebuild - run next commands:

- Run Without clearing volumes(It isn't delete DB)
  - `sudo docker-compose down`
  - `sudo docker-compose build`
  - `sudo docker-compose up` or `sudo docker-compose up -d`
- Run with clearing volumes
  - `sudo docker-compose down -v`
  - `sudo docker-compose build`
  - `sudo docker-compose up` or `sudo docker-compose up -d`

Check logs - use command `sudo docker-compose logs -f`

## Deploy
Firstly need generate ssh key - use command `ssh-keygen`.
Add key to repository settings, tab `Deploy keys`.

1. Clone repository to ubuntu user directory.
2. Go to project folder
3. Go to `deploy` folder
4. Use command `chmod +x ./setup` - its script install Docker and another system packages.
5. Run `./setup`
6. Go to project folder

Change database accesses to production in files `.env.prod`:
- SQL_DATABASE
- SQL_USER
- SQL_PASSWORD
- SITE_URL - set host domain or ip 

Change database accesses to production in files `docker-compose.prod.yml`:
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB

Build server `sudo docker-compose -f docker-compose.prod.yml build`.

Run server `sudo docker-compose -f docker-compose.prod.yml up -d`.

If you have change files - follow commands:

`sudo docker-compose -f docker-compose.prod.yml down` - stop containers without 
clearing volumes (database will not remove)

`sudo docker-compose -f docker-compose.prod.yml down -v` - stop containers with 
clearing volumes (database will remove)

`sudo docker-compose -f docker-compose.prod.yml build` - build containers with new files updates

`sudo docker-compose -f docker-compose.prod.yml up -d` - run server

Create backup database before any actions with docker containers.