import uvicorn
from fastapi import FastAPI

import pl_worker.porch_light as porch_light


class web_app:
    def __init__(self):
        self.app = FastAPI()

        @self.app.get("/")
        async def root():
            return {self.app.docs_url}

        @self.app.get("/check-hub")
        async def check_hub():
            h = porch_light.check_hub()
            return {h}

        @self.app.get("/start")
        async def start():
            from multiprocessing import Process

            background_server = Process(target=porch_light.LightWorker.change_light_color, daemon=True)
            background_server.start()
            return {background_server.pid}


class Server:
    port = 8080

    @classmethod
    def local_nic(cls):
        import socket

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        nic = s.getsockname()[0]
        s.close()
        return nic

    @classmethod
    def start_server(cls):
        u = uvicorn
        c = u.config.Config(app=web_app().app, host=cls.local_nic(), port=cls.port)
        w = u.Server(c)
        w.run()


if __name__ == "__main__":
    Server.start_server()
