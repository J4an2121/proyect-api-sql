# schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

# --- Client ---
class ClientCreate(BaseModel):
    name: str
    email: EmailStr

class ClientOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# --- Product ---
class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock: int

    class Config:
        from_attributes = True


# --- InvoiceItem ---
class InvoiceItemCreate(BaseModel):
    product_id: int
    quantity: int

class InvoiceItemOut(BaseModel):
    product: ProductOut
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True


# --- Invoice ---
class InvoiceCreate(BaseModel):
    client_id: int
    items: List[InvoiceItemCreate]

class InvoiceOut(BaseModel):
    id: int
    date: datetime
    total: float
    client: ClientOut
    items: List[InvoiceItemOut]

    class Config:
        from_attributes = True


### La distinción clave: ORM vs Schema

#Tienes dos representaciones del mismo dato:

#| | Modelo ORM | Schema Pydantic |
#|--|-----------|-----------------|
#| **Archivo** | `models.py` | `schemas.py` |
#| **Hereda de** | `Base` | `BaseModel` |
#| **Para qué** | hablar con la BD | hablar con el usuario |
#| **Valida datos** | no | sí |

#El flujo siempre es:

#Request JSON → Schema (valida) → ORM (guarda en BD)
#BD → ORM (lee) → Schema (responde JSON)