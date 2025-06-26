FROM python:3.12-bullseye
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000:8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]