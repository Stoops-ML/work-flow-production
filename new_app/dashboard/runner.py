import json
import os
from typing import Any

from websockets.sync.client import connect


def runner(
    func: str, module: str, *args, **kwargs
) -> tuple[dict[str, Any], tuple[Any]]:
    packet = {
        "event": "runFunction",
        "inputs": {
            "module": module,
            "function": func,
            "inputs": {"args": args, "kwargs": kwargs},
        },
    }
    with connect(f"ws://localhost:{os.environ['PORT_SERVER']}") as websocket:
        websocket.send(json.dumps(packet))
        message = json.loads(websocket.recv())
    return message["status"], message["results"]
