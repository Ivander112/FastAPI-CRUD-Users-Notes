from fastapi import APIRouter, Depends, Path, Request, Response, HTTPException
from api.base.base_schemas import BaseResponse, PaginationParams
from .schemas import CreateNoteRequest, CreateNoteResponse, NotePaginationResponse, ReadAllNoteResponse,ReadNoteResponse, UpdateNoteRequest, UpdateNoteResponse, DeleteNoteResponse
from .use_cases import CreateNote,ReadAllNote, ReadNote,ReadAllNote, UpdateNote, DeleteNote
from middlewares.authentication import get_user_id_from_access_token

router = APIRouter(prefix="/notes")
tag = "Notes"

@router.post("/add", response_model=CreateNoteResponse, tags=[tag])
async def create(
    request: CreateNoteRequest,
    response: Response,
    create_note: CreateNote = Depends(CreateNote),
    user_id: int = Depends(get_user_id_from_access_token),
) -> CreateNoteResponse:
    try:
        resp_data = await create_note.execute(
            request=request,
            user_id=user_id
        )

        return CreateNoteResponse(
            status="success",
            message="success add new note",
            data=resp_data.dict(),
        )
    except HTTPException as ex:
        # Log HTTPException detail
        response.status_code = ex.status_code
        return CreateNoteResponse(
            status="error",
            message=ex.detail,
        )
    except Exception as e:
        # Log general exception detail
        response.status_code = 500
        message = "failed to add new note"
        return CreateNoteResponse(
            status="error",
            message=message,
        )

@router.get("", response_model=ReadAllNoteResponse, tags=[tag])
async def read_all(
    request: Request,
    response: Response,
    user_id: int = Depends(get_user_id_from_access_token),
    filter_by_user_id: bool = False,
    page_params: PaginationParams = Depends(),
    read_all: ReadAllNote = Depends(ReadAllNote),
) -> ReadAllNoteResponse:
    try:
        resp_data = await read_all.execute(
            page_params=page_params,user_id=user_id, filter_by_user_id=filter_by_user_id
        )

        return ReadAllNoteResponse(
            status="success",
            message="success read users",
            data=NotePaginationResponse(records=resp_data[0], meta=resp_data[1]),
        )
    except HTTPException as ex:
        response.status_code = ex.status_code
        return ReadAllNoteResponse(
            status="error",
            message=ex.detail,
        )
    except Exception as e:
        response.status_code = 500
        message = "failed to read users"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return ReadAllNoteResponse(
            status="error",
            message=message,
        )


@router.get("/{note_id}", response_model=ReadNoteResponse, tags=[tag])
async def read(
    request: Request,
    response: Response,
    note_id: int,
    user_id: int = Depends(get_user_id_from_access_token),
    update_note: ReadNote = Depends(ReadNote),
) -> ReadNoteResponse:
    try:
        resp_data = await update_note.execute(note_id=note_id,user_id=user_id)

        return ReadNoteResponse(
            status="success",
            message="success read note",
            data=resp_data,
        )
    except HTTPException as ex:
        response.status_code = ex.status_code
        return ReadNoteResponse(
            status="error",
            message=ex.detail,
        )
    except Exception as e:
        response.status_code = 500
        message = "failed to read note"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail
        return ReadNoteResponse(
            status="error",
            message=message,
        )

@router.put("/{note_id}", response_model=UpdateNoteResponse, tags=[tag])
async def update(
    request: UpdateNoteRequest,
    response: Response,
    note_id: int,
    user_id: int = Depends(get_user_id_from_access_token),
    update_note: UpdateNote = Depends(UpdateNote),
) -> UpdateNoteResponse:
    try:
        resp_data = await update_note.execute(
            note_id=note_id, user_id=user_id, request=request
        )

        return UpdateNoteResponse(
            status="success",
            message="success update note",
            data=resp_data,
        )
    except HTTPException as ex:
        response.status_code = ex.status_code
        return UpdateNoteResponse(
            status="error",
            message=ex.detail,
        )
    except Exception as e:
        response.status_code = 500
        message = "failed to update note"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail
        return UpdateNoteResponse(
            status="error",
            message=message,
        )

@router.delete("/{note_id}", response_model=DeleteNoteResponse, tags=[tag])
async def delete(
    request: Request,
    response: Response,
    note_id: int,
    user_id: int = Depends(get_user_id_from_access_token),
    update_note: DeleteNote = Depends(DeleteNote),
) -> DeleteNoteResponse:
    try:
        resp_data = await update_note.execute(
            note_id=note_id, user_id=user_id
        )

        return DeleteNoteResponse(
            status="success",
            message="success update note",
            data=resp_data,
        )
    except HTTPException as ex:
        response.status_code = ex.status_code
        return DeleteNoteResponse(
            status="error",
            message=ex.detail,
        )
    except Exception as e:
        response.status_code = 500
        message = "failed to update note"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail
        return DeleteNoteResponse(
            status="error",
            message=message,
        )