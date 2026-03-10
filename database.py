from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./billing.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para inyectar la sesión en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#create_engine — conecta Python con la BD. El arg check_same_thread=False es necesario solo con SQLite (permite múltiples requests).
#SessionLocal — es la fábrica de sesiones. Cada request abre una sesión, hace su trabajo, y la cierra.
#Base — clase base de la que van a heredar todos tus modelos ORM.
#get_db() — el patrón yield garantiza que la sesión siempre se cierra, incluso si hay un error. La vas a usar con Depends() en los endpoints.