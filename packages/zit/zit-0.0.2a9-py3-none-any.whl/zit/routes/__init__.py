from fastapi import APIRouter

from ..dataset.manager import Manager
from .dataset.annotations import build_annotations_router
from .dataset.categories import build_categories_router
from .dataset.images import build_images_router
from .dataset.queries import build_queries_router


def build_default_router(params, manager: Manager):
    r = APIRouter(prefix="/default")

    r.include_router(build_images_router(params, manager))
    r.include_router(build_annotations_router(params, manager))
    r.include_router(build_categories_router(params, manager))
    r.include_router(build_queries_router(params, manager))

    return r


__all__ = ["build_default_router"]
