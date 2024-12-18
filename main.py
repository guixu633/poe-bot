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

app = FastAPI()
bot = EchoBot()

# 创建 Poe bot 应用并挂载到 FastAPI
poe_app = fp.make_app(
    bot, 
    access_key='y9HC3Tp1McPH8yMoT4WY93W7KpQkqmlv', 
    bot_name='EchoBotGVRJM7UIV0'
)
app.mount("/", poe_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
