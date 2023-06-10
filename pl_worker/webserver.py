import json
import logging
import os
import time

import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse, RedirectResponse

import pl_worker
import pl_worker.porch_light as porch_light

if os.getenv("LOG_LEVEL") is None:
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=int(os.getenv("LOG_LEVEL")))


class web_app:
    def __init__(self):
        self.app = FastAPI()

        @self.app.get("/", include_in_schema=False)
        async def root():
            return RedirectResponse(self.app.docs_url)

        @self.app.get(
            "/check-hub",  # For AutoDocs
            responses={
                status.HTTP_200_OK: {"description": "Connection to hub OK"},
                status.HTTP_503_SERVICE_UNAVAILABLE: {
                    "description": "Cannot connect to hub",
                },
            },
        )
        async def check_hub():
            h = porch_light.check_hub()
            if h.host is not None:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content="OK",
                )
            else:
                return JSONResponse(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    content="Cannot get Hubitat",
                )

        @self.app.get("/start")
        async def start():  # pragma: no cover # TODO Remove when test fixed
            from multiprocessing import Process

            background_server = Process(target=porch_light.LightWorker.change_light_color, daemon=True)
            background_server.start()
            while background_server.is_alive():
                time.sleep(1)
            import pl_worker

            p_obj = pl_worker.porch_light.LightWorker()
            p_obj.pre_load_color()
            r = json.dumps({"EXITCODE": background_server.exitcode})
            if background_server.exitcode == 0:
                return JSONResponse(status_code=status.HTTP_200_OK, content=r)
            else:
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=r)


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
    def start_server(cls):  # pragma: no cover # TODO Remove when test fixed
        u = uvicorn
        c = u.config.Config(app=web_app().app, host=cls.local_nic(), port=cls.port, proxy_headers=True)
        w = u.Server(c)
        w.run()


if __name__ == "__main__":
    p = pl_worker.porch_light.LightWorker()
    p.pre_load_color()
    Server().start_server()
