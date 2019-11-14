import unittest
import json
from app.message_constants import (
    RequestMessageID, ResponseMessageID, Message, MessageEncoder, MessageDecoder
)

class TestRequestMessageID(unittest.TestCase):
    def test_is_json_serializable(self):
        try:
            json.dumps(RequestMessageID.LIST_GAMES)
        except TypeError as error:
            self.fail(str(error))
        

class TestResponseMessageID(unittest.TestCase):
    def test_is_json_serializable(self):
        try:
            json.dumps(ResponseMessageID.GAME_CREATED)
        except TypeError as error:
            self.fail(str(error))


class TestMessage(unittest.TestCase):
    def test_is_json_serializable(self):
        message_null_body = Message(RequestMessageID.CREATE_GAME, None)
        message_list_body = Message(RequestMessageID.CREATE_GAME, [1, 2, 3, 4])
        message_dict_body = Message(RequestMessageID.CREATE_GAME, {'x': 1, 'y': 2})

        try:
            json.dumps(message_null_body, cls=MessageEncoder)
            json.dumps(message_list_body, cls=MessageEncoder)
            json.dumps(message_dict_body, cls=MessageEncoder)
        except TypeError as error:
            self.fail(str(error))

    def test_is_json_deserializable(self):
        request = Message(RequestMessageID.CREATE_GAME, {'name': 'my game'})
        response = Message(ResponseMessageID.GAME_CREATED, {'name': 'game name'})
        encoded_request = json.dumps(request, cls=MessageEncoder)
        encoded_response = json.dumps(response, cls=MessageEncoder)

        try:
            decoded_request = json.loads(encoded_request, cls=MessageDecoder)
            decoded_response = json.loads(encoded_response, cls=MessageDecoder)
        except TypeError as error:
            self.fail(str(error))

        self.assertEqual(request.message_id, decoded_request.message_id)
        self.assertEqual(request.body, decoded_request.body)
        self.assertEqual(response.message_id, decoded_response.message_id)
        self.assertEqual(response.body, decoded_response.body)