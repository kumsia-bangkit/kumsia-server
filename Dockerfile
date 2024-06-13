# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# Copy the GCP service account key into the container
COPY /home/c010d4kx0675/key/kumsia-key.json /code/gcp-key.json

# Set the environment variable for GCP credentials
ENV GOOGLE_APPLICATION_CREDENTIALS="/code/gcp-key.json"

# Make port 2134 available to the world outside this container
EXPOSE 2134

# Run main.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "2134"]