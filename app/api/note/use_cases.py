import datetime
import math
from typing import Annotated

from fastapi import Depends, HTTPException

from sqlalchemy import select, desc, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession

from db import get_session
from api.base.base_schemas import PaginationMetaResponse, PaginationParams
from models.note import Note, NoteSchema
from .schemas import CreateNoteRequest, UpdateNoteRequest

# async def get_sorted_notes_from_database(session: Session):
#     async with session.begin():
#         sorted_notes = session.execute(select(Note).order_by(desc(Note.note_id)))
#         sorted_notes = sorted_notes.scalars().all()

#         # Print note IDs for debugging purposes
#         for note in sorted_notes:
#             print(f"Note ID: {note.note_id}")

#         return sorted_notes


AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]

class CreateNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, request: CreateNoteRequest, user_id: int) -> NoteSchema:
        try:
            async with self.async_session() as session:
                note_exists = await session.execute(
                    select(Note).where(Note.title == request.title)
                )
                print(user_id)
                note_exists = note_exists.scalar()
                if note_exists is not None:
                    raise HTTPException(
                        status_code=400, detail=f"Title '{request.title}' is already taken"
                    )

                note = Note(
                    title=request.title,
                    content=request.content,
                    created_by=user_id
                )

                session.add(note)
                await session.flush()
                await session.commit()
                await session.refresh(note)

                # Hanya mengembalikan sebagian atribut yang diinginkan dari NoteSchema
            return NoteSchema.from_orm(note)
        
        except Exception as e:
            # Print exception information
            print(f"An error occurred while executing CreateNote: {e}")
            raise e

class ReadAllNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    
    async def execute(
        self,
        user_id: int,
        page_params: PaginationParams,
        filter_by_user_id: bool,
    ) -> (list[NoteSchema], PaginationMetaResponse):
        async with self.async_session() as session:
            total_item_query = (
                select(func.count())
                .select_from(Note)
                .where(Note.deleted_at == None)
            )

            if filter_by_user_id:
                total_item_query = total_item_query.filter(Note.created_by == user_id)

            total_item = await session.execute(total_item_query)
            total_item = total_item.scalar()

            query = (
                select(Note)
                .where(Note.deleted_at == None)
                .offset((page_params.page - 1) * page_params.item_per_page)
                .limit(page_params.item_per_page)
            )

            if filter_by_user_id:
                query = query.filter(Note.created_by == user_id)

            paginated_query = await session.execute(query)
            paginated_query = paginated_query.scalars().all()

            notes = [NoteSchema.from_orm(note) for note in paginated_query]

            meta = PaginationMetaResponse(
                total_item=total_item,
                page=page_params.page,
                item_per_page=page_params.item_per_page,
                total_page=math.ceil(total_item / page_params.item_per_page),
            )

            return notes, meta


class ReadNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, note_id: int) -> NoteSchema:
        async with self.async_session() as session:
            query = select(Note).where(
                (Note.note_id == note_id).__and__(Note.deleted_at == None)
            )
            
            note = await session.execute(query)
            note = note.scalars().first()
            if not note:
                raise HTTPException(status_code=404)

            return NoteSchema.from_orm(note)

import logging

logger = logging.getLogger(__name__)

# use_cases.py

class UpdateNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, note_id: int, user_id: int, request: UpdateNoteRequest) -> NoteSchema:
        try:
            async with self.async_session() as session: 
                note = await session.execute(
                    select(Note).where(
                        (Note.note_id == note_id).__and__(Note.deleted_at == None)
                    ).order_by(Note.note_id) 
                )
                note = note.scalars().first()
                if not note:
                    raise HTTPException(status_code=404)

                title_is_modified = note.title != request.title
                if title_is_modified:
                    nt = await session.execute(  # Mengganti variabel u menjadi nt
                        select(Note).where(Note.title == request.title)
                    )
                    nt = nt.scalars().first()
                    if nt is not None:
                        raise HTTPException(
                            400, f"title: {request.title} is already taken"
                        )

                content_is_modified = note.content != request.content
                if content_is_modified:
                    nt = await session.execute(  # Mengganti variabel u menjadi nt
                        select(Note).where(Note.content == request.content)
                    )
                    nt = nt.scalars().first()
                    if nt is not None:
                        raise HTTPException(400, f"content: {request.content} is already taken")


                note.title = request.title
                note.content = request.content
                note.updated_at = datetime.datetime.utcnow()
                note.updated_by = user_id

                await session.flush()
                await session.commit()
                await session.refresh(note)

                # sorted_notes = get_sorted_notes_from_database(session)

                return NoteSchema.from_orm(note)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail="failed to update note")

class DeleteNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, note_id: int, user_id: int) -> NoteSchema:
        try:
            async with self.async_session() as session: 
                note = await session.execute(
                    select(Note).where(
                        (Note.note_id == note_id).__and__(Note.deleted_at == None)
                    ).order_by(Note.note_id) 
                )
                note = note.scalars().first()
                if not note:
                    raise HTTPException(status_code=404)
                
                note.deleted_at= datetime.datetime.utcnow()
                note.deleted_by = user_id

                await session.flush()
                await session.commit()
                await session.refresh(note)

                # sorted_notes = get_sorted_notes_from_database(session)

                return NoteSchema.from_orm(note)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail="failed to update note")