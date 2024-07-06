import unittest

from pydantic import ValidationError

import app
from app.schemas.external_services_schemas.chatbot import (
    AssistantResponse,
    ChatMessage,
    Conversation,
)


class TestChatModels(unittest.TestCase):

    def test_conversation(self):
        conversation = Conversation(assistant_id="assistant_id", thread_id="thread_id")
        self.assertEqual(conversation.assistant_id, "assistant_id")
        self.assertEqual(conversation.thread_id, "thread_id")

    def test_assistant_response(self):
        response = AssistantResponse(
            role="assistant", message="Hello, how can I help you?"
        )
        self.assertEqual(response.role, "assistant")
        self.assertEqual(response.message, "Hello, how can I help you?")

    def test_chat_message(self):
        chat_message = ChatMessage(text="This is a message.")
        self.assertEqual(chat_message.text, "This is a message.")
