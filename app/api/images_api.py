from fastapi import APIRouter, status, HTTPException
from fastapi.responses import FileResponse
from core.library import *

router = APIRouter()

@router.get("/images/{hash}")
async def images_api(hash: str, size: int | str = 'orig') -> FileResponse:
    image_hash = await hash_to_image(hash)
    try:
        image_path = await LibraryTasks.get_images(image_hash, size)
        if image_path:
            return FileResponse(image_path)
        else:
            image_path = await LibraryTasks.get_images(hash, size)
            if image_path: return FileResponse(image_path)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=err)