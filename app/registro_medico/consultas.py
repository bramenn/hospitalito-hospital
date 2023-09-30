from aws_client import enviar_evento_reportar_receta
from fastapi import status
from fastapi.exceptions import HTTPException

from .. import db
from ..medicos.consultas import obtener_medico_cc_db
from ..pacientes.consultas import obtener_paciente_cc_db
from ..pacientes.modelo import PacienteOut
from .modelo import (
    HistoriaClinica,
    HistoriaClinicaIn,
    HistoriaClinicaOut,
    RecetaMedica,
    RecetaMedicaIn,
    RecetaMedicaOut,
    RegistroMedico,
    RegistroMedicoIn,
    RegistroMedicoOut,
)


def obtener_historia_clinica_cc_db(cc: str) -> HistoriaClinicaOut:
    paciente: PacienteOut = obtener_paciente_cc_db(cc=cc)

    historia_clinica = (
        db.session.query(HistoriaClinica).where(HistoriaClinica.id_paciente == paciente.id).first()
    )

    if not historia_clinica:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Historia clinica no econtrada",
        )

    return parsear_historia_clinica(historia_clinica, paciente)


def obtener_registro_medico_id_db(id: int) -> RegistroMedicoOut:
    registro_medico = db.session.query(RegistroMedico).where(RegistroMedico.id == id).first()

    if not registro_medico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Registro medico no econtrado"
        )

    return parsear_registro_medico(registro_medico)


def obtener_receta_medica_id_db(id: int) -> RecetaMedicaOut:
    receta_medica = db.session.query(RecetaMedica).where(RecetaMedica.id == id).first()

    if not receta_medica:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Receta medica no econtrada"
        )

    return parsear_receta_medica(receta_medica)


def crear_historia_clinica_db(
    nueva_historia_clinica: HistoriaClinicaIn,
) -> HistoriaClinicaOut:
    paciente: PacienteOut = obtener_paciente_cc_db(cc=nueva_historia_clinica.cedula_paciente)
    historia_clinica = None

    try:
        historia_clinica = obtener_historia_clinica_cc_db(cc=paciente.cedula)
    except:
        pass

    if historia_clinica:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Paciente ya con historia clinica",
        )

    historia_clinica = HistoriaClinica(id_paciente=paciente.id)

    try:
        db.session.add(historia_clinica)
        db.session.commit()
        historia_clinica = obtener_historia_clinica_cc_db(cc=paciente.cedula)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se ha creado la historia clinica",
        )

    return historia_clinica


def crear_receta_medica_db(nueva_receta_medica: RecetaMedicaIn) -> RecetaMedicaOut:
    receta_medica = RecetaMedica(
        medicamento=nueva_receta_medica.medicamento,
        dosis=nueva_receta_medica.dosis,
        frecuencia=nueva_receta_medica.frecuencia,
        id_registro_medico=nueva_receta_medica.id_registro_medico,
    )

    try:
        db.session.add(receta_medica)
        db.session.commit()
        receta_medica = obtener_receta_medica_id_db(receta_medica.id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se ha creado la receta medica",
        )

    return receta_medica


def crear_registro_medico_db(registro_medico_in: RegistroMedicoIn):
    paciente = obtener_paciente_cc_db(cc=registro_medico_in.cedula_paciente)

    medico = obtener_medico_cc_db(cc=registro_medico_in.cedula_medico)

    try:
        historia_clinica = obtener_historia_clinica_cc_db(cc=paciente.cedula)
    except:
        historia_clinica = crear_historia_clinica_db(
            HistoriaClinicaIn(cedula_paciente=paciente.cedula)
        )

    registro_medico = RegistroMedico(
        descripcion=registro_medico_in.descripcion,
        id_historia_clinica=historia_clinica.id,
        id_medico=medico.id,
    )

    try:
        db.session.add(registro_medico)
        db.session.commit()

        registro_medico = obtener_registro_medico_id_db(registro_medico.id)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se ha creado el registro medico",
        )

    if registro_medico_in.medicamentos:
        for medicamento in registro_medico_in.medicamentos:
            receta_medica = crear_receta_medica_db(
                RecetaMedicaIn(
                    medicamento=medicamento.nombre,
                    dosis=medicamento.dosis,
                    frecuencia=medicamento.frecuencia,
                    id_registro_medico=registro_medico.id,
                )
            )

            try:
                enviar_evento_reportar_receta(
                    {
                        "id_registro_medico": registro_medico.id,
                        "cedula_paciente": paciente.cedula,
                        "nombre_paciente": f"{paciente.nombre} {paciente.apellidos}",
                        "email_paciente": paciente.email,
                        "telefono_paciente": paciente.celular,
                        "cedula_medico": medico.cedula,
                        "nombre_medico": f"{medico.nombre} {medico.apellidos}",
                        "hospital": "La 40",
                        "dosis": receta_medica.dosis,
                        "frecuencia": receta_medica.frecuencia,
                        "medicamento": receta_medica.medicamento,
                        "id_receta_medica_hospitalito": receta_medica.id,
                        "id_sucursal": registro_medico_in.id_sucursal,
                    },
                    registro_medico_in.id_sucursal,
                )

            except Exception as e:
                print(f"Error enviando receta media a sns: {e}")

    return obtener_historia_clinica_cc_db(cc=paciente.cedula)


def receta_entregada_id_db(id: int) -> RecetaMedicaOut:
    receta_medica = db.session.query(RecetaMedica).where(RecetaMedica.id == id).first()
    receta_medica.entregado = True

    try:
        db.session.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se ha actualizado el estado de la receta",
        )

    return obtener_receta_medica_id_db(id)


def parsear_registro_medico(registro_medico: RegistroMedico) -> RegistroMedicoOut:
    return RegistroMedicoOut(
        id=registro_medico.id,
        descripcion=registro_medico.descripcion,
        id_medico=registro_medico.id_medico,
        created_date=registro_medico.created_date,
        recetas=[parsear_receta_medica(receta) for receta in registro_medico.recetas_medicas],
    )


def parsear_receta_medica(receta_medica: RecetaMedica) -> RecetaMedicaOut:
    return RecetaMedicaOut(
        id=receta_medica.id,
        medicamento=receta_medica.medicamento,
        dosis=receta_medica.dosis,
        frecuencia=receta_medica.frecuencia,
        entregado=receta_medica.entregado,
    )


def parsear_historia_clinica(
    historia_clinica: HistoriaClinica, paciente: PacienteOut
) -> HistoriaClinicaOut:
    return HistoriaClinicaOut(
        id=historia_clinica.id,
        paciente=paciente,
        registros_medicos=[
            parsear_registro_medico(registro_medico)
            for registro_medico in historia_clinica.registros_medicos
        ],
    )
