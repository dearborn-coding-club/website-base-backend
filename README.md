# Dearborn Coding Club's Backend Django Server
- A backend webserver for serving static assets and handling requests for dearborncodingclub.com.
- Check out the slack channel [here](https://dearborncodingclub.slack.com).
- Check out the meetup group [here](https://www.meetup.com/dearborn-coding-club).

## Getting Set Up In Docker (Recommended)
- Ensure you have docker [desktop installed locally](https://www.docker.com/products/docker-desktop/).
- Run `docker login`.
- Run `docker run -p 8000:8000 --rm -it $(docker build -q .)`.
    - Optionally, you can run `make run`.
- Go to http://localhost:8000 in your web browser and view the website locally! 🎉

## Running the application on a different domain
- If you want to run the application on a different domain, be sure to add to the `settings.py` file under `ALLOWED_HOSTS`.

## Deploy
- Right now, only the owner of the `fly.io` can deploy. In the future, we'd like the deployment to occur when merging a pull request.
- Install `flyctl`
    - `brew install flyctl`.
- Run `flyctl deploy`.
