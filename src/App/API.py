import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .OrderController import order_router

# from .UserController import user_router


def run_app():
    app = FastAPI(
        title="Food delivery API",
        description="Order, menu and delivery management for a catering service.",
    )

    # Enregistrement des routers
    # app.include_router(auth_router, prefix="/auth")  # Routes d'authentification
    app.include_router(order_router, prefix="/orders")  # Routes pour les clients
    # app.include_router(menu_router, prefix="/menus")  # Routes pour l'admin
    # app.include_router(delivery_router, prefix="/deliveries")  # Routes pour les livreurs

    @app.get("/", include_in_schema=False)
    async def redirect_to_docs():
        return RedirectResponse(url="/docs")

    uvicorn.run(app, port=5000, host="0.0.0.0")
