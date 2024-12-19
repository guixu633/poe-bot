from fastapi import FastAPI
import uvicorn
from chat import router as chat_router

app = FastAPI()

# 注册路由
app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
