from sqlalchemy import Column, Integer, String
import db

from pydantic import BaseModel


class Medico(db.Base):
    __tablename__ = "medico"
    id = Column("id", Integer, autoincrement=True, primary_key=True, unique=True)
    cedula = Column("cedula", String(255), index=True)
    nombre = Column("nombre", String(255))
    apellidos = Column("apellidos", String(255))
    espcialidad = Column("espcialidad", String(255))


class MedicoOut(BaseModel):
    id: int
    cedula: str
    nombre: str
    apellidos: str
    espcialidad: str


class MedicoIn(BaseModel):
    cedula: str
    nombre: str
    apellidos: str
    espcialidad: str
