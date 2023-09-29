from fastapi import APIRouter
from .modelo import (
    RegistroMedicoIn,
    HistoriaClinicaOut,
    HistoriaClinicaIn,
    RecetaMedicaOut,
)
from .consultas import (
    obtener_historia_clinica_cc_db,
    crear_historia_clinica_db,
    crear_registro_medico_db,
    receta_entregada_id_db,
)

router = APIRouter()


@router.get("/historia_clinica/{cc}", response_model=HistoriaClinicaOut)
def obtener_historia_clinica_cc(cc: str):
    return obtener_historia_clinica_cc_db(cc=cc)


@router.post("/medico", response_model=HistoriaClinicaOut)
def crear_receta_medica(registro_medico: RegistroMedicoIn):
    return crear_registro_medico_db(registro_medico)


@router.post("/historia_clinica", response_model=HistoriaClinicaOut)
def crear_historia_clinica(nueva_historia_clinica: HistoriaClinicaIn):
    return crear_historia_clinica_db(nueva_historia_clinica)


@router.put("/receta_entregada/{id}", response_model=RecetaMedicaOut)
def receta_entregada(id: str):
    return receta_entregada_id_db(id)
