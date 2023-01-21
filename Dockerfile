# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

# Run an update
RUN apt-get update

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script file
COPY app.py .

# Run the script every five minutes after the hour using cron
RUN echo "*/5 * * * * /usr/local/bin/python /app/app.py" > /etc/cron.d/script-cron
RUN chmod 0644 /etc/cron.d/script-cron

# Run cron in the foreground
CMD ["cron", "-f"]