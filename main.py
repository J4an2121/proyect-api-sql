# main.py
import sys
import os
sys.path.append(os.path.dirname(__file__))  # ← agrega la raíz al path

from fastapi import FastAPI
from database import engine, Base
import models
from routers import clients, products, invoices

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Billing API")

app.include_router(clients.router)
app.include_router(products.router)
app.include_router(invoices.router)

@app.delete("/reset", tags=["Dev"])
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"message": "Base de datos reiniciada"}