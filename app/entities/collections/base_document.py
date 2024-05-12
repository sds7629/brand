from bson import ObjectId
from pydantic import dataclasses

from app.config import Config


@dataclasses.dataclass(kw_only=True, config=Config)
class BaseDocument:
    _id: ObjectId

    @property
    def id(self) -> ObjectId:
        return self._id
