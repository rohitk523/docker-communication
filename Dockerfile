# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install pandas
# 
COPY ./FastAPI/app /code/app1
COPY ./docker/app /code/app2

# 
CMD ["uvicorn", "app1.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
CMD ["uvicorn", "app2.main:app", "--host", "0.0.0.0", "--port", "8086", "--reload"]
