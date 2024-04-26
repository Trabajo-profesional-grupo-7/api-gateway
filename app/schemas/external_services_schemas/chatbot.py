from pydantic import BaseModel


class Conversation(BaseModel):
    assistant_id: str
    thread_id: str


class AssistantResponse(BaseModel):
    role: str
    message: str


class ChatMessage(BaseModel):
    text: str
