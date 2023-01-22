# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

# Run an update
RUN apt-get update

# Install cron
RUN apt-get install -y cron

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script file
COPY app.py .

# Run the script every five minutes after the hour using cron
# RUN echo "*/5 * * * * /usr/local/bin/python /app/app.py" > /etc/cron.d/script-cron

# Create log file
RUN touch /var/log/script-cron.log

# RUN echo "*/5 * * * * root /usr/local/bin/python /app/app.py >> /var/log/script-cron.log 2>&1" >> /etc/cron.d/script-cron
# RUN echo "*/5 * * * * root /usr/local/bin/python /app/app.py >> /proc/1/fd/1 2>/proc/1/fd/2 /var/log/script-cron.log" >> /etc/cron.d/script-cron
RUN echo "*/5 * * * * root /usr/local/bin/python /app/app.py | tee -a /var/log/script-cron.log /proc/1/fd/1 2>/proc/1/fd/2" >> /etc/cron.d/script-cron


RUN chmod 0644 /etc/cron.d/script-cron

# Pipe environment variables from docker container level to cron environment level and run cron in foreground
CMD ["/bin/bash", "-c", "printenv > /etc/environment && cron -f"]