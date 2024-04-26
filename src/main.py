from dotenv import load_dotenv
from fastapi import FastAPI

from chat import base_chat, completion, file_chat

load_dotenv()


def mount_app_routes(app: FastAPI):
    app.post(
        "/chat/completion",
        tags=["chat"],
        summary="单次对话"
    )(completion)

    app.post(
        "/chat/llm_chat",
        tags=["chat"],
        summary="多轮对话"
    )(base_chat)

    app.post(
        "/chat/file_chat",
        tags=["chat"],
        summary="文件对话"
    )(file_chat)


app = FastAPI(
    title="Chat-your-file",
    version="1.0.0",
)
mount_app_routes(app)
