from pydantic import BaseModel

class TranscriptRequest(BaseModel):
    transcript: str

class MoMResponse(BaseModel):
    summary: str
    key_discussions: list
    decisions: list 
    action_items: list