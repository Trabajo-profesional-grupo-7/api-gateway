from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.routers.attractions.attractions_router import router as attraction_router
from app.routers.external_services.external_services_router import (
    router as external_services_router,
)
from app.routers.notifications.notifications_router import (
    router as notifications_router,
)
from app.routers.users.authentication_router import router as authentication_router
from app.routers.users.password_router import router as password_router
from app.routers.users.users_router import router as users_router

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

app.include_router(authentication_router)
app.include_router(users_router)
app.include_router(password_router)
app.include_router(attraction_router)
app.include_router(external_services_router)
app.include_router(notifications_router)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")
