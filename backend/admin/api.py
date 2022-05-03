from ninja import NinjaAPI
from django_ninja.api import router as ninja_router

api = NinjaAPI(
    title="API Docs"
)
api.add_router('', ninja_router)
