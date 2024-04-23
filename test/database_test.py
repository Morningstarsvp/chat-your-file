import uuid

from database import *

message = MessageModel(
    conversation_id=uuid.uuid4().hex,
    chat_type='test',
    query='query',
    response='response'
)

message2 = MessageModel(
    id=1,
    conversation_id=uuid.uuid4().hex,
    chat_type='aaaaaaa',
    query='111111',
    response='modify response'
)

upsert_message(message)
# print(get_messages())
# message = get_message_by_id(1)
# message.response = 'modify response'
# print(get_messages())