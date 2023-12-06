import uuid
import shutil
import hashlib
from typing import List
from pathlib import Path

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, status, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse

from src.db.models import File
from src.schemas.file import FileRetrieveSchema
from src.routers.deps import get_db_session, get_authenticated_user


file_router = APIRouter(prefix='/files', tags=['File'])

# file_router.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@file_router.get("/download/uploads/{folder_name}/{file_name}/")
async def download_file(folder_name: str, file_name: str):
    file_path = Path(f"uploads/{folder_name}/{file_name}")
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path)

@file_router.post('/upload/', status_code=status.HTTP_201_CREATED, response_model=List[FileRetrieveSchema])
async def upload_files(
        files: List[UploadFile],
        db_session: Session = Depends(get_db_session),
        current_user = Depends(get_authenticated_user)
):

    hash_md5 = hashlib.md5(f'user_id-{current_user.id}'.encode('utf-8')).hexdigest()
    base_path = Path(f'uploads/{hash_md5}')
    base_path.mkdir(parents=True, exist_ok=True)

    uploaded_files = []

    for file in files:
        filename = f'{uuid.uuid4()}-{file.filename}'
        upload_path = base_path / filename
        try:
            with upload_path.open('wb') as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_on_db = File(
                name=filename,
                content_type=file.content_type,
                upload_path=str(upload_path),
            )
            file_on_db.save(db_session)
            uploaded_files.append(file_on_db)
        except SQLAlchemyError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Erro ao salvar o arquivo'
            )

    return uploaded_files
