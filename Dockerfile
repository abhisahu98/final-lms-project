FROM python:3.10-slim

RUN apt-get update && apt-get install -y netcat-openbsd dos2unix && apt-get clean

WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy and fix permissions
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh
RUN ls -l /app/wait-for-it.sh

COPY . /app

# Start command
CMD ["sh", "./wait-for-it.sh", "db:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
