from fastapi import FastAPI
import uvicorn

from pacientes import endpoint as pacientes_endpoint
from medicos import endpoint as medicos_enpoint
from registro_medico import endpoint as registro_medico_endpoint
from db import Base, conn

app = FastAPI()


app.include_router(pacientes_endpoint.router, prefix="/v1/paciente", tags=["pacientes"])
app.include_router(medicos_enpoint.router, prefix="/v1/medico", tags=["medicos"])
app.include_router(
    registro_medico_endpoint.router, prefix="/v1/registro", tags=["registro"]
)


if __name__ == "__main__":
    Base.metadata.create_all(conn)

    uvicorn.run(app="main:app", reload=True)
