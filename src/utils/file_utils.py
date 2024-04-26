def extract_contents(data):
    all_contents = ""
    for item in data:
        contents = item.get('contents', [])
        for content_item in contents:
            if content_item.get('type') != 'image':
                all_contents += content_item['content']
    # 返回包含所有内容的字符串
    return all_contents

#
# from langchain_community.vectorstores import Chroma
#
# from config import EMBEDDING_FUNCTIONS, EMBEDDING_MODEL
# from text_splitter import ChineseRecursiveTextSplitter
#
# with open(r"D:\Code\chat-your-file\src\data\resolved.txt", 'r', encoding='utf-8') as fp:
#     data = fp.read()
#
# splitter = ChineseRecursiveTextSplitter(chunk_size=1024, chunk_overlap=128)
# text = splitter.split_text(data)
# embedding = EMBEDDING_FUNCTIONS.get(EMBEDDING_MODEL)
# collection_name = "test"
# persist_directory = "D:\Code\chat-your-file\src\knowledge_base" + "\\" + collection_name
# Chroma.from_texts(
#     text,
#     embedding=embedding,
#     collection_name="test",
#     persist_directory=persist_directory
# )
#
# from database import crud, schemas
#
# vs_collection = schemas.VSCollectionBase(
#     collection_name=collection_name,
#     persist_directory=persist_directory,
#     embedding_function=EMBEDDING_MODEL
# )
# crud.create_vs_collection(vs_collection)
