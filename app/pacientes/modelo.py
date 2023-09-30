from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from .. import db


class Paciente(db.Base):
    __tablename__ = "paciente"
    id = Column("id", Integer, autoincrement=True, primary_key=True, unique=True)
    cedula = Column("cedula", String(255), index=True)
    nombre = Column("nombre", String(255))
    apellidos = Column("apellidos", String(255))
    celular = Column("celular", String(255))
    email = Column("email", String(255))


class PacienteIn(BaseModel):
    cedula: str
    nombre: str
    apellidos: str
    celular: str
    email: str


class PacienteOut(BaseModel):
    id: int
    cedula: str
    nombre: str
    apellidos: str
    celular: str
    email: str
