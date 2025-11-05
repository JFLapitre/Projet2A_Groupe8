import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .OrderController import order_router
from .UserController import user_router


def run_app():
    app = FastAPI(
        title="Food delivery API",
        description="Order, menu and delivery management for a catering service.",
    )

    # Enregistrement des routers
    # app.include_router(auth_router, prefix="/auth")
    app.include_router(user_router, prefix="/users")
    app.include_router(order_router, prefix="/orders")
    # app.include_router(menu_router, prefix="/menus")
    # app.include_router(delivery_router, prefix="/deliveries")

    @app.get("/", include_in_schema=False)
    async def redirect_to_docs():
        return RedirectResponse(url="/docs")

    uvicorn.run(app, port=5000, host="0.0.0.0")
