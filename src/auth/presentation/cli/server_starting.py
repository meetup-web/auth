from click import argument, option
from dishka import FromDishka
from dishka.integrations.click import inject
from uvicorn import Server as UvicornServer


@argument("path", default=None, required=False)
@option("-h", "--host", default=None, help="The server host")
@option("-p", "--port", default=None, type=int, help="The server port")
@inject
def start_uvicorn(
    path: str | None,
    host: str | None,
    port: int | None,
    *,
    uvicorn_server: FromDishka[UvicornServer],
) -> None:
    if path is not None:
        uvicorn_server.config.app = path

    if host is not None:
        uvicorn_server.config.host = host

    if port is not None:
        uvicorn_server.config.port = port

    uvicorn_server.run()
