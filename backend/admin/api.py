from ninja import NinjaAPI
from ninja.api import router as router

api = NinjaAPI(
    title="API Docs"
)
api.add_router('', router)