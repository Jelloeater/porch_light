import uvicorn
from fastapi import FastAPI

import pl_worker.porch_light


class web_app:
    def __init__(self):
        self.app = FastAPI()

        @self.app.get("/")
        async def root():
            return {self.app.docs_url}

        @self.app.get("/check-hub")
        async def root():
            h = pl_worker.porch_light.check_hub()
            return {h}


def start_server():
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_nic = s.getsockname()[0]
    s.close()
    uvicorn.run(web_app().app, host=local_nic, port=8080)


if __name__ == "__main__":
    start_server()
