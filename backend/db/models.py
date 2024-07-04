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

class Trabajador(Base):
    __tablename__ = 'trabajador_taller'

    dni = Column(String(8), index=True, primary_key=True)

class Tiempo(Base):
    __tablename__='tiempo'

    dni = Column()
    fecha = Column()
    hora_entrada = Column()
    hora_salida = Column()

class Personal(Base):
    __tablename__='personal_administrativo'

    dni = Column()
    salario = Column()

class Pago(Base):
    __tablename__='pago'

    codigo = Column()
    fecha = Column()

class Deposito(Base):
    __tablename__='deposito_pago'

    codigo = Column()
    pago_codigo = Column()
    dni = Column()

class Pago_Personal(Base):
    __tablename__='pago_personal_administrativo'

    dni = Column()
    codigo = Column()

class Pago_Trabajador(Base):
    __tablename__='pago_trabajador_taller'

    dni = Column()
    codigo = Column()
    horas_semana = Column()
    monto = Column()

class Ubicacion(Base):
    __tablename__='ubicacion'

    codigo = Column()
    salario = Column()