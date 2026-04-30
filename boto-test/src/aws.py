from enum import Enum
import boto3
from src.config import settings


class S3Session():
    session = boto3.session.Session()
    client = None

    @classmethod
    def get_client(cls):
        if cls.client is None:
            cls.client = cls.session.client(
                service_name="s3",
                endpoint_url=settings.S3_URL,  # Замените на реальный адрес вашего сервиса
                aws_access_key_id=settings.S3_KEY_ID,
                aws_secret_access_key=settings.S3_SECRET_KEY,
                region_name=settings.S3_REGION  # Регион зависит от документации вашего поставщика
            )
        return cls.client


class FileTypeEnum(str, Enum):
    image = "image"   # фотографии
    video = "video"   # видео
    docs = "docs"   # документы
    text = "text"   # текст


class S3Func:
    client = S3Session.get_client()

    @classmethod
    def upload(cls, upload_file, path=''):
        try:
            cls.client.put_object(
                Body=upload_file.file,  # Путь до файла на компе
                Bucket=settings.S3_BUCKET_NAME,
                Key=f'{path}{upload_file.filename}'  # Путь
            )
            return "Файл успешно загружен!"
        except Exception as e:
            raise f"Ошибка при загрузке файла: {e}"

    @classmethod
    def delete(cls, delete_file_name, path=''):
        try:
            cls.client.delete_object(
                Bucket=settings.S3_BUCKET_NAME,
                Key=f'{path}{delete_file_name}'
            )
            return "Файл успешно удален!"
        except Exception as e:
            raise f"Ошибка при загрузке файла: {e}"

    @classmethod
    def get_all_object_names(cls):
        response = cls.client.list_objects_v2(Bucket=settings.S3_BUCKET_NAME)
        if 'Contents' in response:
            names = [obj['Key'] for obj in response['Contents']]
            return names
        else:
            print("Бакет пуст")

    @staticmethod
    def filter(text):
        if text in ['txt']:
            return FileTypeEnum.text
        elif text in ['doc', 'docx']:
            return FileTypeEnum.docs
        elif text in ['mp4', 'mov', 'avi', 'mkv']:
            return FileTypeEnum.video
        elif text in ['jpeg', 'png', 'gif', 'tiff', 'webp']:
            return FileTypeEnum.image
