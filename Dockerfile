# Dockerfile
FROM python:3.10-slim

# Install required dependencies
RUN apt-get update && apt-get install -y netcat-openbsd dos2unix && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy and fix permissions for wait-for-it.sh
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Copy application code
COPY . /app

# Define the command to run the application
CMD ["bash", "./wait-for-it.sh", "db:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
