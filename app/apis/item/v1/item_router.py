from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId


router = APIRouter(prefix="/items", tags=["items"], redirect_slashes=False)


