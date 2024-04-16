# Dearborn Coding Club's Backend Django Server
- A backend webserver for serving static assets and handling requests for dearborncodingclub.com.

## Getting Set Up
First, install direnv, as specified in the installation docs. ([docs](https://direnv.net/docs/installation.html)).

Next, install pyenv, and add $HOME/.pyenv/bin to the path of your respective shell. Then install Python 3.11.2
(or whatever version of Python is decided on for this repository).

Then, cd into the root directory of this repository and then type

```sh
direnv allow
```

## How to run dev server
- Cd into `/server`
     - `cd server`
- Run `python manage.py runserver` or `python3 manage.py runserver` depending on where your python3 is located.
- More documentation on how to set this up can be found [here](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment).
