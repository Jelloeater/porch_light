import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def start_server():
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_nic = s.getsockname()[0]
    s.close()
    uvicorn.run(app, host=local_nic, port=8080)


if __name__ == "__main__":
    start_server()
