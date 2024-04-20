# Dearborn Coding Club's Backend Django Server
- A backend webserver for serving static assets and handling requests for dearborncodingclub.com.

## Getting Set Up In Docker (Recommended)
- Ensure you have docker [desktop installed locally](https://www.docker.com/products/docker-desktop/).
- Run `docker run -p 8000:8000 --rm -it $(docker build -q .)`.
## Getting Set Up Locally (Not complete 🙅🏾)
- First, install direnv, as specified in the installation docs. ([docs](https://direnv.net/docs/installation.html)).
     - As of the latest docs, you can run `curl -sfL https://direnv.net/install.sh | bash`.
- Brew install poetry with `brew install poetry`
     - Run `peotry install` from the root of the project.
     - Run `eval "$(direnv hook zsh)"`
     - Run `eval "$(pyenv virtualenv-init -)"`
- Next, install pyenv, and add `$HOME/.pyenv/bin` to the path of your respective shell. Then install Python 3.11.2
     - Install `pyenv` with 
     `brew update` and then
     `brew install pyenv`
(or whatever version of Python is decided on for this repository).

- Then, cd into the root directory of this repository and then type

     ```sh
     direnv allow
     ```

## How to run dev server
- Cd into `/server`
     - `cd server`
- Run `python manage.py runserver` or `python3 manage.py runserver` depending on where your python3 is located.
- More documentation on how to set this up can be found [here](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment).
