from io import BytesIO
from typing import Any, BinaryIO

import boto3
from fastapi import File, UploadFile
from PIL import Image

from app.config import FSO_ACCESS_KEY, FSO_SECRET_KEY

s3 = boto3.client(
    "s3",
    aws_access_key_id=FSO_ACCESS_KEY,
    aws_secret_access_key=FSO_SECRET_KEY,
    region_name="ap-northeast-2",
)


def upload_image_to_s3(file: BinaryIO, bucket_name: str, file_name: str) -> None:
    s3.upload_fileobj(
        file,
        bucket_name,
        file_name,
        ExtraArgs={"ContentType": "image/jpeg"},
    )


def convert_to_bytes(image: Image) -> BytesIO:
    img_byte = BytesIO()
    image.save(img_byte, "JPEG", quality=90)
    img_byte.seek(0)
    return img_byte


async def validate_image_file(file: UploadFile) -> UploadFile:
    if file.filename.split(".")[-1].lower() not in ["jpg", "jpeg", "png"]:
        raise ValueError("Only jpg, jpeg and png files are supported")
    return file


async def upload_image(file: UploadFile = File(...)) -> dict[Any, Any]:
    if not file:
        return {"detail": "파일이 없습니다."}
    image_file = await validate_image_file(file)

    import uuid

    file_name = f"{str(uuid.uuid4())}.jpg"
    s3_key = f"image/{file_name}"
    upload_image_to_s3(
        file.file,
        "fsobucket",
        s3_key,
    )
    import urllib

    return {
        "url": "https://fsobucket.s3-ap-northeast-2.amazonaws.com/%s" % (urllib.parse.quote(s3_key, safe="~()*!.'"))
    }
