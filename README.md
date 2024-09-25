# Dearborn Coding Club's Backend Django Server
A Django backend API webserver for serving static assets and handling requests for dearborncodingclub.com. It is currently hooked up to https://api.dearborncodingclub.com/notes.


## Architecture
```
website-base-backend/
|--- Dockerfile         # Docker configuration
|--- Makefile           # Helper file to run scripts
|--- manage.py          # Used to run Django server
|--- core/              # Core Django app functionionalities
    |--- migrations/
    |--- templatetags/
    |--- admin.py
    |--- apps.py
    |--- models.py
    |--- serializers.py
    |--- tests.py
    |--- views.py
|--- public_api         # `api.dearborncodingclub` funcitonalities
    |--- asgi.py
    |--- settings.py
    |--- urls.py
    |--- views.py
    |--- wsgi.py
|--- server             # Database config?
```

Feel free to check out the slack channel [here](https://dearborncodingclub.slack.com) and our meetup group [here](https://www.meetup.com/dearborn-coding-club).

## Getting Set Up In Docker (Recommended)
- Ensure you have docker [desktop installed locally](https://www.docker.com/products/docker-desktop/).
- Run `docker login`.
- Run `docker run -p 8000:8000 --rm -it $(docker build -q .)`.
    - Optionally, you can run `make run`.

## Getting Set Up For Mac
1. Make sure you install `python3` on your local machine and  have a virtual environment set up.
    - Run python environment
        - `python3 -m venv ./`.
    - Upgrade pip
        - `python3 -m pip install --upgrade pip`.
    - Install python dependencies
        - `python3 -m pip install -r requirements.txt`.
    - Install django-cors-headers
        - `python3 -m pip install django-cors-headers==4.3.1`.
    
    - Activate local python env.
        - `source bin/activate`.
    - If you don't have the `python3` alias set, configure the from alias `python3` to `python`.
        - `echo 'alias python="python3"' >> ~/.zshrc && source ~/.zshrc;`
2. Run the application.
    - Run `make run` or
    - Run `python manage.py runserver`.
- Go to http://localhost:8000 in your web browser and view backend endpoint locally.

## Deploying to Fly.io
We currently use [Fly.io](https://fly.io) run the service.

We deploy the app via GitHub Actions whenever a PR merges into main (points to https://api.dearborncodingclub.com).
 
You can also deploy the application manually by executing `flyctl deploy` from the repo folder, after logging in to an admin account locally (`flyctl auth login`).
- You can install the `flyctl` CLI tool too.

## (Re)generating TLS Certificates
[Fly.io](https://fly.io) handles our TLS certificates as part of their managed hosting service. We have manually generated a Let's Encrypt certificate using:

`fly certs add dearborncodingclub.com`

## Running the application on a different domain
- If you want to run the application on a different domain, be sure to add to the `settings.py` file under `ALLOWED_HOSTS`.