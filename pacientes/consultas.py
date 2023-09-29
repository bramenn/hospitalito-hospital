import db
from fastapi import status
from .modelo import Paciente, PacienteIn, PacienteOut
from fastapi.exceptions import HTTPException


def obtener_paciente_cc_db(cc: str) -> PacienteOut:
    paciente = db.session.query(Paciente).where(Paciente.cedula == cc).first()

    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado"
        )

    return parsear_paciente(paciente)


def crear_paciente_db(nuevo_paciente: PacienteIn) -> PacienteOut:
    try:
        paciente = obtener_paciente_cc_db(nuevo_paciente.cedula)
    except Exception:
        paciente = None

    if paciente:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="El paciente ya existe"
        )

    paciente = Paciente(
        cedula=nuevo_paciente.cedula,
        nombre=nuevo_paciente.nombre,
        apellidos=nuevo_paciente.apellidos,
        celular=nuevo_paciente.celular,
        email=nuevo_paciente.email,
    )

    try:
        db.session.add(paciente)
        db.session.commit()
        return parsear_paciente(paciente)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se ha creado el paciente",
        )


def parsear_paciente(paciente: Paciente) -> PacienteOut:
    return PacienteOut(
        id=paciente.id,
        cedula=paciente.cedula,
        nombre=paciente.nombre,
        apellidos=paciente.apellidos,
        celular=paciente.celular,
        email=paciente.email,
    )
