FROM python:3.12.4-bookworm
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000