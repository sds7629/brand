from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse
from starlette.responses import Response

router = APIRouter(prefix="/v1/users", tags=["users"], redirect_slashes=False)
