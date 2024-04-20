FROM python:3.9.19-bookworm
WORKDIR ./
COPY . .
# RUN curl -sSL https://install.python-poetry.org | python3 -
RUN pip install -r requirements.txt
# RUN cd server
WORKDIR ./server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000