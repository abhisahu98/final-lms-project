# Use Python 3.10 slim image
FROM python:3.10-slim

# Install necessary packages
RUN apt-get update && apt-get install -y netcat-openbsd dos2unix && apt-get clean

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Fix permissions and line endings for wait-for-it.sh
COPY wait-for-it.sh /app/wait-for-it.sh
RUN dos2unix /app/wait-for-it.sh && chmod +x /app/wait-for-it.sh

# Default command to start the app
CMD ["./wait-for-it.sh", "db:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
