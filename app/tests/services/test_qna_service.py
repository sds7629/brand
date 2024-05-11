from app.services.qna_service import find_qna_by_title, find_qna_by_id, qna_list


async def test_find_qna_by_title_service() -> None:
    title = "안녕하세요"

    result = await find_qna_by_title(title)

    assert len(result) == 2


async def test_find_qna_all() -> None:
    result = await qna_list()

    assert len(result) == 2
