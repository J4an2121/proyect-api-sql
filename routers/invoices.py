from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.post("/", response_model=schemas.InvoiceOut)
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == invoice.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    db_invoice = models.Invoice(client_id=invoice.client_id)
    db.add(db_invoice)
    db.flush()  # genera el id sin hacer commit aún

    total = 0.0
    for item in invoice.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Producto {item.product_id} no encontrado")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para {product.name}")

        unit_price = product.price
        db_item = models.InvoiceItem(
            invoice_id=db_invoice.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=unit_price,
        )
        product.stock -= item.quantity
        total += unit_price * item.quantity
        db.add(db_item)

    db_invoice.total = total
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

@router.get("/{invoice_id}", response_model=schemas.InvoiceOut)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return invoice