from fastapi import APIRouter
from .consultas import obtener_medico_cc_db, crear_medico_db

from .modelo import MedicoOut, MedicoIn

router = APIRouter()


@router.get("/{cc}", response_model=MedicoOut)
def obtener_medico(cc: str):
    medico = obtener_medico_cc_db(cc)
    return medico


@router.post("/", response_model=MedicoOut)
def crear_medico(nuevo_medico: MedicoIn):
    medico = crear_medico_db(nuevo_medico)

    return medico
