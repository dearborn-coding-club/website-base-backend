# Dearborn Coding Club's Backend Django Server
- A backend webserver for serving static assets and handling requests for dearborncodingclub.com.
- Check out the slack channel [here](https://dearborncodingclub.slack.com).
- Check out the meetup group [here](https://www.meetup.com/dearborn-coding-club).

## Getting Set Up In Docker (Recommended)
- Ensure you have docker [desktop installed locally](https://www.docker.com/products/docker-desktop/).
- Run `docker login`.
- Run `docker run -p 8000:8000 --rm -it $(docker build -q .)`.
    - Optionally, you can run `make run`.

## For Mac
- Install pnpm
    - `curl -fsSL https://get.pnpm.io/install.sh | sh -`.
- Install python dependencies
    - `python3 -m pip install -r requirements.txt`.
- Install django-cors-headers
    - `python3 -m pip install django-cors-headers==4.3.1`.
- Run python environment
    - `python3 -m venv ./`.
- Upgrade pip
    - `python3 -m pip install --upgrade pip`.
- Activate local python env.
    - `source bin/activate`.
- If you need, alias `python3` to `python`.
    - `echo 'alias python="python3"' >> ~/.zshrc && source ~/.zshrc;`

- Go to http://localhost:8000 in your web browser and view the website locally! 🎉

## Running the application on a different domain
- If you want to run the application on a different domain, be sure to add to the `settings.py` file under `ALLOWED_HOSTS`.

## Deploy
- To deploy changes to the website (dearborncodingclub.com), merge a pull request to `main`.
- In order to deploy changes to the website manually, make sure you're logged into the fly.io site (https://fly.io/apps/website-base-backend) locally.
- Install `flyctl`
    - `brew install flyctl`.
- Run `flyctl deploy`.
