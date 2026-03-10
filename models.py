# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    invoices = relationship("Invoice", back_populates="client")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    items = relationship("InvoiceItem", back_populates="product")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, default=0.0)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    client = relationship("Client", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product", back_populates="items")


### ¿Qué hace cada parte?

#`__tablename__`** — nombre de la tabla en la BD.

#**`ForeignKey("clients.id")`** — llave foránea, referencia a otra tabla.

#**`relationship()`** — le dice a SQLAlchemy cómo navegar entre modelos en Python. No es una columna en la BD, es solo para tu código.

#**`back_populates`** — conecta la relación en ambos lados. Si accedes a `invoice.client` obtienes el objeto `Client`, y desde `client.invoices` obtienes su lista de facturas.

#**`InvoiceItem`** — es la tabla intermedia entre `Invoice` y `Product`. Guarda cantidad y precio unitario al momento de la venta (importante: el precio puede cambiar después).

#---

### Relaciones resumidas
#```
#Client ──< Invoice ──< InvoiceItem >── Product