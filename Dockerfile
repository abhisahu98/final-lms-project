FROM python:3.10-slim
RUN apt-get update && apt-get install -y netcat-openbsd dos2unix && apt-get clean
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["sh", "./wait-for-it.sh", "db:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
