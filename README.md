# Dearborn Coding Club's Backend Django Server
- A backend webserver for serving static assets and handling requests for dearborncodingclub.com.

## Getting Set Up In Docker (Recommended)
- Ensure you have docker [desktop installed locally](https://www.docker.com/products/docker-desktop/).
- Run `docker login`.
- Run `docker run -p 8000:8000 --rm -it $(docker build -q .)`.
- Go to http://localhost:8000 in your web browser and view the website locally! 🎉

## To deploy
- install `flyctl`
    - `brew install flyctl`
- run `flyctl deploy`