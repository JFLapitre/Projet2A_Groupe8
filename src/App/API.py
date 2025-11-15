import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routers.AuthController import auth_router
from .routers.MenuController import menu_router
from .routers.OrderController import order_router
from .routers.UserController import user_router


def run_app():
    app = FastAPI(
        title="UB'EJR Eats",
        description="Admin API for menu management, consulting orders and creating driver and admin accounts",
    )

    # Enregistrement des routers
    app.include_router(auth_router)
    app.include_router(menu_router)
    app.include_router(order_router)
    app.include_router(user_router)

    @app.get("/", include_in_schema=False)
    async def redirect_to_docs():
        return RedirectResponse(url="/docs")

    uvicorn.run(app, port=5000, host="0.0.0.0")
