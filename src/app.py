import uvicorn
from fastapi import FastAPI

from chat import base_chat


def mount_app_routes(app: FastAPI):
    app.post(
        "/chat/llm_chat",
        tags=["chat"],
        summary="模型对话"
    )(base_chat)


if __name__ == "__main__":
    app = FastAPI(
        title="Chat-your-file",
        version="1.0.0",
    )
    mount_app_routes(app)
    uvicorn.run(app, host="0.0.0.0", port=8000)
