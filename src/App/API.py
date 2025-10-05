import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse


#from .OrderController import order_router
#from .UserController import user_router



def run_app():
    app = FastAPI(
        title="API de Livraison de Repas",
        description="Gestion des commandes, menus et livraisons pour un service de restauration."
    )

    # Enregistrement des routers
    #app.include_router(auth_router, prefix="/auth")      # Routes d'authentification
    #app.include_router(order_router, prefix="/orders")   # Routes pour les clients
    #app.include_router(menu_router, prefix="/menus")     # Routes pour l'admin
    #app.include_router(delivery_router, prefix="/deliveries")  # Routes pour les livreurs

    @app.get("/", include_in_schema=False)
    async def redirect_to_docs():
        return RedirectResponse(url="/docs")

    uvicorn.run(app, port=8000, host="0.0.0.0")