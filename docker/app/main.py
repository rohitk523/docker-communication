from fastapi import FastAPI, Request

app = FastAPI()


@app.get('/')
def read_root():
    return {'Heloo World'}


@app.post('/requests')
async def req(request: Request):
    #r = requests.get('http://127.0.0.1:8000/user')
    data = await request.json()
    file1 = open("myfile.txt", "a")  # append mode
    try:
        file1.write(f"User {data['name']} uploaded file {data['filename']} at timestamp {data['time']} with wordcount {data['wordcount']} \n")
    finally:
        file1.close()
    return {'success'}

# User X uploaded file Y at timestamp with wordcount z