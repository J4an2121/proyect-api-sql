# proyect-api-sql
REST API de facturación empresarial con FastAPI, SQLAlchemy y SQLite. CRUD de clientes, productos y facturas con cálculo automático de totales y descuento de inventario.
# Billing API

REST API de facturación empresarial construida con FastAPI y SQLAlchemy.

## Tecnologías
- Python + FastAPI
- SQLAlchemy + SQLite
- Pydantic

## Endpoints
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/clients/` | Crear cliente |
| GET | `/clients/` | Listar clientes |
| POST | `/products/` | Crear producto |
| GET | `/products/` | Listar productos |
| POST | `/invoices/` | Crear factura |
| GET | `/invoices/{id}` | Ver factura |

## Instalación
```bash
pip install fastapi uvicorn sqlalchemy pydantic[email]
uvicorn main:app --reload
```

Documentación interactiva en `http://localhost:8000/docs`
