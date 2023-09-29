from typing import List, Optional
import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
import db

from medicos.modelo import Medico
from pacientes.modelo import PacienteOut

from pydantic import BaseModel


class RecetaMedica(db.Base):
    __tablename__ = "receta_medica"
    id = Column("id", Integer, autoincrement=True, primary_key=True, unique=True)
    medicamento = Column("medicamento", String(255))
    dosis = Column("dosis", Integer)
    frecuencia = Column("frecuencia", Integer)
    entregado = Column(Boolean, unique=False, default=False)
    id_registro_medico = Column(Integer, ForeignKey("registro_medico.id"))


class RegistroMedico(db.Base):
    __tablename__ = "registro_medico"
    id = Column("id", Integer, autoincrement=True, primary_key=True, unique=True)
    descripcion = Column("descripcion", String(500))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    id_historia_clinica = Column(Integer, ForeignKey("historia_clinica.id"))
    id_medico = Column(Integer, ForeignKey("medico.id"))

    recetas_medicas = relationship(RecetaMedica)


class HistoriaClinica(db.Base):
    __tablename__ = "historia_clinica"
    id = Column("id", Integer, autoincrement=True, primary_key=True, unique=True)
    id_paciente = Column(Integer, ForeignKey("paciente.id"), unique=True)
    registros_medicos = relationship(RegistroMedico)


class MedicamentosBase(BaseModel):
    nombre: str
    dosis: int
    frecuencia: int


class RegistroMedicoIn(BaseModel):
    cedula_paciente: str
    cedula_medico: str
    descripcion: str
    medicamentos: Optional[List[MedicamentosBase]] = []

    id_sucursal: int


class HistoriaClinicaIn(BaseModel):
    cedula_paciente: str


class RecetaMedicaIn(BaseModel):
    medicamento: str
    dosis: int
    frecuencia: int
    entregado: bool = False
    id_registro_medico: int


class RecetaMedicaOut(BaseModel):
    id: int
    medicamento: str
    dosis: int
    frecuencia: int
    entregado: bool


class RegistroMedicoOut(BaseModel):
    id: int
    descripcion: str
    id_medico: int
    created_date: datetime.datetime
    recetas: Optional[List[RecetaMedicaOut]]


class HistoriaClinicaOut(BaseModel):
    id: int
    paciente: PacienteOut
    registros_medicos: List[RegistroMedicoOut]
