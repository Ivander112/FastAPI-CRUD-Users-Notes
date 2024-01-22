from pydantic import BaseModel, Field, EmailStr
from api.base.base_schemas import BaseResponse, PaginationMetaResponse
from utils import REGEX_PASSWORD

from models.note import NoteSchema

# Create note
class CreateNoteRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=6, max_length=100)

class CreateNoteResponse(BaseResponse):
    data: dict | None

# Get note
    
class ReadNoteResponse(BaseResponse):
    data: dict | None

# Get all note

class NotePaginationResponse(BaseModel):
    records: list[NoteSchema]
    meta: PaginationMetaResponse

class ReadAllNoteResponse(BaseResponse):
    data: NotePaginationResponse

# Update note
    
class UpdateNoteRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=6, max_length=100)

class UpdateNoteResponse(BaseResponse):
    data: dict | None

# Deleted Note

class DeleteNoteResponse(BaseResponse):
    data: dict | None