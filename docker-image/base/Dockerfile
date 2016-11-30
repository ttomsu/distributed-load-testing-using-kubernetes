# Start with a base Python 2.7.8 image
FROM python:2.7.8

# Add the external tasks directory into /tasks
ADD requirements.txt requirements.txt

# Install the required dependencies via pip
RUN pip install -r requirements.txt

# Expose the required Locust ports
EXPOSE 5557 5558 8089
