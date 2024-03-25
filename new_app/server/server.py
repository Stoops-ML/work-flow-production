import asyncio
import importlib
import json
import os
import sys
from typing import Any

from websockets.legacy.server import WebSocketServerProtocol
from websockets.server import serve


PACKAGE_NAME = __package__.split(".")[0]


async def receive(websocket: WebSocketServerProtocol) -> None:
    async for ws_message in websocket:
        try:
            packet: dict[str, Any] = json.loads(ws_message)
            match packet["event"]:
                case "runFunction":
                    try:
                        module = sys.modules.get(
                            ".".join((PACKAGE_NAME, packet["inputs"]["module"])),
                            importlib.import_module(
                                "." + packet["inputs"]["module"], package=PACKAGE_NAME
                            ),
                        )
                        func = getattr(module, packet["inputs"]["function"])
                        results = func(
                            *packet["inputs"]["inputs"]["args"],
                            **packet["inputs"]["inputs"]["kwargs"],
                        )
                        if not isinstance(results, tuple):
                            results = (results,)
                        status, err_msg = True, ""
                    except Exception as e:
                        status = False
                        err_msg = ": ".join((type(e).__name__, str(e)))
                        results = tuple()
                case _:
                    status = False
                    err_msg = f"Error: event {packet['event']} not recognised"
                    results = tuple()
        except Exception as e:
            status = False
            err_msg = f"Error: {str(e)}"
            results = tuple()
        await websocket.send(
            json.dumps(
                {"status": {"pass": status, "errMsg": err_msg}, "results": results}
            )
        )


async def main():
    async with serve(
        receive, "localhost", int(os.environ["PORT_SERVER"]), max_size=None
    ):
        await asyncio.Future()


def start_server():
    asyncio.run(main())


if __name__ == "__main__":
    start_server()
