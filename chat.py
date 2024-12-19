from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import fastapi_poe as fp
import json
import os


router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    temperature: Optional[float] = 0
    messages: List[Message]

class ChatResponse(BaseModel):
    model: str
    choices: List[dict]

# 添加 security scheme
security = HTTPBearer()

@router.post("/v1/chat/completions")
async def chat_completions(
    request: ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        # 从 bearer token 中获取 API key
        api_key = credentials.credentials

        # 将请求消息转换为 POE 协议消息
        poe_messages = [
            fp.ProtocolMessage(role=msg.role, content=msg.content)
            for msg in request.messages
        ]

        
        
        # 收集完整响应
        full_response = ""
        async for text in get_responses(poe_messages, api_key, request.model):
            full_response += text

        # 构造响应
        response = ChatResponse(
            model=f"{request.model}",
            choices=[
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": full_response
                    }
                }
            ]
        )
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 修改函数签名，移除 api_key 参数，添加 bot_name 参数
async def get_responses(messages, api_key, bot_name="GPT-3.5-Turbo"):
    async for partial in fp.get_bot_response(messages=messages, bot_name=bot_name, api_key=api_key):
        response_dict = partial.raw_response
        inner_json = json.loads(response_dict['text'])
        yield inner_json['text']

if __name__ == "__main__":
    message = fp.ProtocolMessage(role="user", content="Hello world")
    
    api_key = os.getenv('POE_API_KEY')
    if not api_key:
        raise ValueError("请设置环境变量 POE_API_KEY")

    async def main():
        async for text in get_responses([message],api_key):
            print(text, end='', flush=True)
        print('\n')
    
    asyncio.run(main())
