from __future__ import annotations
from typing import AsyncIterable
import fastapi_poe as fp
from fastapi import FastAPI

class EchoBot(fp.PoeBot):
    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        last_message = request.query[-1].content
        yield fp.PartialResponse(text=last_message)

if __name__ == "__main__":
    import sys
    sys.argv.extend(["-p", "8002"])
    fp.run(
        EchoBot(),
        access_key='y9HC3Tp1McPH8yMoT4WY93W7KpQkqmlv'
    )