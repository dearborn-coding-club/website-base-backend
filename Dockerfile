FROM python:3.12.4-bookworm
WORKDIR ./
COPY . .
# RUN curl -sSL https://install.python-poetry.org | python3 -
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt
# RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
# USER docker
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000