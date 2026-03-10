from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=schemas.ClientOut)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Client).filter(models.Client.email == client.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    db_client = models.Client(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/", response_model=list[schemas.ClientOut])
def list_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()