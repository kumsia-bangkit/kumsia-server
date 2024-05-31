# 
FROM python:3.9

# 
WORKDIR /

# 
COPY ./requirements.txt /requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# 
COPY ./app /app

# Make port 2134 available to the world outside this container
EXPOSE 2134

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "2134"]