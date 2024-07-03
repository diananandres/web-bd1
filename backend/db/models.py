from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    PrimaryKeyConstraint,
    ForeignKeyConstraint
)

from db.db_setup import Base

from sqlalchemy.orm import relationship

class Empleado(Base):
    __tablename__ = 'empleado'

    dni = Column(String(8), index=True, primary_key=True)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    fecha_contratacion = Column(Date, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
