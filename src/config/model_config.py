from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_zhipu import ZhipuAIEmbeddings

CHAT_MODEL = "glm4"
TEMPERATURE = 0.3
EMBEDDING_MODEL = "bge-m3"

# 嵌入模型映射
EMBEDDING_FUNCTIONS = {
    "embedding-v2": ZhipuAIEmbeddings(),
    "bge-m3": HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": "cpu"},
        encode_kwargs={'normalize_embeddings': True}
    ),
}