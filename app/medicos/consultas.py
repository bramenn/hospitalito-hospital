from fastapi import status
from fastapi.exceptions import HTTPException

from .. import db
from .modelo import Medico, MedicoIn, MedicoOut


def obtener_medico_cc_db(cc: str) -> MedicoOut:
    medico = db.session.query(Medico).where(Medico.cedula == cc).first()

    if not medico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medico no encontrado")

    return parsear_medico(medico)


def crear_medico_db(nuevo_medico: MedicoIn) -> MedicoOut:
    try:
        medico = obtener_medico_cc_db(nuevo_medico.cedula)
    except Exception:
        medico = None

    if medico:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="El medico ya existe"
        )

    medico = Medico(
        cedula=nuevo_medico.cedula,
        nombre=nuevo_medico.nombre,
        apellidos=nuevo_medico.apellidos,
        espcialidad=nuevo_medico.espcialidad,
    )

    try:
        db.session.add(medico)
        db.session.commit()
        return parsear_medico(medico)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se ha creado el medico",
        )


def parsear_medico(medico: Medico) -> MedicoOut:
    return MedicoOut(
        id=medico.id,
        cedula=medico.cedula,
        nombre=medico.nombre,
        apellidos=medico.apellidos,
        espcialidad=medico.espcialidad,
    )
