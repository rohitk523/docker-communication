# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

#
COPY ./test_main.py /code/test_main.py

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./FastAPI/app /code/FastAPI/app
COPY ./docker/app /code/docker/app

# 
CMD ["uvicorn", "FastAPI.app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
CMD ["uvicorn", "docker.app.main:app", "--host", "0.0.0.0", "--port", "8086", "--reload"]
