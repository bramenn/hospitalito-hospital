from fastapi import APIRouter
from .consultas import obtener_paciente_cc_db, crear_paciente_db

from .modelo import PacienteIn, PacienteOut

router = APIRouter()


@router.get("/{cc}", response_model=PacienteOut)
def obtener_paciente(cc: str):
    paciente = obtener_paciente_cc_db(cc)
    return paciente


@router.post("/", response_model=PacienteOut)
def crear_paciente(nuevo_paciente: PacienteIn):
    paciente = crear_paciente_db(nuevo_paciente)

    return paciente
