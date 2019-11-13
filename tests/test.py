import unittest
import json
from app.message_constants import RequestMessageID, ResponseMessageID, Message

class TestRequestMessageID(unittest.TestCase):

    def test_is_json_serializable(self):
        try:
            json.dumps(RequestMessageID.LIST_GAMES)
        except TypeError:
            self.fail('RequestMessageID not JSON serializable')
        

class TestResponseMessageID(unittest.TestCase):

    def test_is_json_serializable(self):
        try:
            json.dumps(ResponseMessageID.GAME_CREATED)
        except TypeError:
            self.fail('ResponseMessageID not JSON serializable')


# class TestMessage(unittest.TestCase):

#     def test_is_json_serializable(self):
#         try:
#             json.dumps(Message(RequestMessageID.CREATE_GAME, ''))
#         except TypeError:
#             self.fail('Message not JSON serializable')