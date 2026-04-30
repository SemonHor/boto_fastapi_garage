import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.routing import APIRouter

from src.aws import S3Func
from src.config import APP_VERSION, settings

router = APIRouter(prefix=settings.BASE_ROUTE_PATH)

app = FastAPI(
    title="S3 TEST",
    version=APP_VERSION,
    openapi_url=f"{settings.BASE_ROUTE_PATH}/openapi.json",
    docs_url=f"{settings.BASE_ROUTE_PATH}/docs"
)


@router.get('/version', tags=['app info'])
async def get_app_info():
    return APP_VERSION


@router.post('/s3/upload')
async def upload(file: UploadFile, path: str = ''):
    return S3Func.upload(file, path)


@router.delete('/s3/delete')
async def delete(filename: str, path: str = ''):
    return S3Func.delete(filename, path)


@router.get('/s3/watch')
async def get_all():
    return S3Func.get_all_object_names()


app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='localhost',
        port=8000,
        reload=True,
    )
