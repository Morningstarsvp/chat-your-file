COMPLETION_DEFAULT = """{query}"""
LLM_CHAT_DEFAULT = """The following is a friendly conversation between a human and an AI. The AI is talkative and 
provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully 
says it doesn't know. Current conversation:\n{chat_history}\nHuman:{query}\nAI:"""
FILE_CHAT_DEFAULT = """You are an assistant for question-answering tasks. Use the following pieces of retrieved 
context to answer the question. If you don't know the answer, just say that you don't know. 
Chat History:{chat_history}\n
Question: {question} \n
Context: {context} \n
Answer:"""

PROMPT_TEMPLATES = {
    "completion": {
        "default": COMPLETION_DEFAULT
    },
    "llm_chat": {
        "default": LLM_CHAT_DEFAULT
    },
    "file_chat": {
        "default": FILE_CHAT_DEFAULT
    }
}


