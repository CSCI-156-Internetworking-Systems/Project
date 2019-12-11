import socket
import json
from enum import IntEnum, unique
from typing import Union, Dict, List

class MessageID(IntEnum):
    pass

# message IDs that come from client:
@unique
class RequestMessageID(MessageID):
    JOIN_SERVER = 0
    GET_AVAILABLE_GAMES = 1
    CREATE_GAME = 2
    JOIN_GAME = 3

# response message IDs:
@unique
class ResponseMessageID(MessageID):
    JOIN_SERVER_SUCCESS = 0
    JOIN_SERVER_ERROR = 1
    GET_AVAILABLE_GAMES_SUCCESS = 2
    GET_AVAILABLE_GAMES_ERROR = 3
    GAME_CREATED = 5
    GAME_LIST = 6


class Message:
    def __init__(self, message_id: MessageID, body: Union[str, Dict, List, None]):
        self.message_id = message_id
        self.body       = body


class MessageEncoder(json.JSONEncoder):
    """Used to serialize a message with the json.dumps function.
    
    To serialize a Message object, use json.dumps(msg, cls=MessageEncoder).
    """
    def default(self, obj: Message):
        if not isinstance(obj, Message):
            # Let the base class raise the TypeError
            return json.JSONEncoder.default(self, obj)

        if isinstance(obj.message_id, RequestMessageID):
            return {
                '__request__': {
                    'id': obj.message_id,
                    'body': obj.body
                }
            }

        elif isinstance(obj.message_id, ResponseMessageID):
            return {
                '__response__': {
                    'id': obj.message_id,
                    'body': obj.body
                }
            }


class MessageDecoder(json.JSONDecoder):
    """Used to deserialize a serialized message with the json.loads function.

    To deserialize a message, use json.loads(serialized, cls=MessageDecoder).
    """

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.as_message, *args, **kwargs)

    def as_message(self, obj):
        if '__request__' in obj:
            request = obj['__request__']
            message_id = RequestMessageID(request['id'])
            body = request['body']
            return Message(message_id, body)

        if '__response__' in obj:
            response = obj['__response__']
            message_id = ResponseMessageID(response['id'])
            body = response['body']
            return Message(message_id, body)

        return obj
            

# connection - some socket object for the message to be sent through
# id - the ID of the message to tell the receiver what the message is about, i.e. what to do with the data
# data - some object, such as a string or array
def sendMSG(connection, id, data):
    outJSON = {"id": id, "data": data}
    connection.send(str.encode(json.dumps(outJSON)))
