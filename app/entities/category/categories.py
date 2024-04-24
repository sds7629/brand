import dataclasses

from app.entities.category.category_codes import CategoryCode


@dataclasses.dataclass
class Category:
    code: str
    name: str


CATEGORIES: dict[CategoryCode, Category] = {
    CategoryCode.TOP: Category(code=CategoryCode.TOP, name="상의"),
    CategoryCode.BOTTOM: Category(code=CategoryCode.BOTTOM, name="하의"),
    CategoryCode.OUTER: Category(code=CategoryCode.OUTER, name="외투"),
}
