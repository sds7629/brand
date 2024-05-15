from app.dtos.qna.qna_request import QnARequest
from app.entities.collections import UserCollection
from app.services.qna_service import (
    create_qna,
    find_qna_by_id,
    find_qna_by_title,
    qna_list,
)


async def test_find_qna_by_title_service() -> None:
    title = "안녕하세요"

    result = await find_qna_by_title(title)

    assert len(result) == 2


async def test_find_qna_all() -> None:
    result = await qna_list()

    assert len(result) == 2


async def test_create_qna_service() -> None:
    title = "안녕하세요"
    payload = "안녕하세요 진우입니다."
    writer = await UserCollection.find_by_nickname("admin")

    qna = QnARequest(title, payload, password=None, image_url=None)

    result = await create_qna(qna, writer)

    assert result.title == title
