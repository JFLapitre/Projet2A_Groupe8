import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# from .OrderController import order_router
# from .UserController import user_router

app = FastAPI(
    title="API de Livraison de Repas",
    description="Gestion des commandes, menus et livraisons pour un service de restauration.",
    version="0.1.0",
    root_path=os.getenv("ROOT_PATH", ""),  # Important pour SSPCloud
)

# Configuration CORS pour SSPCloud
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routers
# app.include_router(auth_router, prefix="/auth")
# app.include_router(order_router, prefix="/orders")
# app.include_router(menu_router, prefix="/menus")
# app.include_router(delivery_router, prefix="/deliveries")

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


# Fonction pour lancer en local uniquement
def run_app():
    uvicorn.run(app, port=8000, host="0.0.0.0")


# Pour le développement local
if __name__ == "__main__":
    run_app()

"""def run_app():
    app = FastAPI(
        title="API de Livraison de Repas",
        description="Gestion des commandes, menus et livraisons pour un service de restauration.",
        root_path=os.getenv("ROOT_PATH", ""),
    )

    # Enregistrement des routers
    # app.include_router(auth_router, prefix="/auth")      # Routes d'authentification
    # app.include_router(order_router, prefix="/orders")   # Routes pour les clients
    # app.include_router(menu_router, prefix="/menus")     # Routes pour l'admin
    # app.include_router(delivery_router, prefix="/deliveries")  # Routes pour les livreurs

    @app.get("/", include_in_schema=False)
    async def redirect_to_docs():
        return RedirectResponse(url="/docs")

    uvicorn.run(app, port=8000, host="0.0.0.0")"""
