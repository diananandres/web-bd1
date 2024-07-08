from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    UniqueConstraint,
    Date,
    Time,
    ForeignKey,
    ForeignKeyConstraint,
    CheckConstraint
)

from db.db_setup import Base

from sqlalchemy.orm import relationship

class Empleado(Base):
    __tablename__ = 'empleado'
    dni = Column(String(8), primary_key=True, nullable=False)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    fecha_contratacion = Column(Date, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)

class TrabajadorTaller(Base):
    __tablename__ = 'trabajador_taller'
    dni = Column(String(8), ForeignKey('empleado.dni'), primary_key=True, nullable=False)
    tarifa = Column(DECIMAL(10, 2), nullable=False)
    __table_args__ = (
        CheckConstraint('tarifa BETWEEN 12 AND 15', name='tarifa_tt_rango'),
        UniqueConstraint('dni', name='dni_tt_unique')
    )

class Tiempo(Base):
    __tablename__ = 'tiempo'
    fecha = Column(Date, primary_key=True, nullable=False)
    dni = Column(String(8), ForeignKey('trabajador_taller.dni'), primary_key=True, nullable=False)
    hora_entrada = Column(Time, nullable=False)
    hora_salida = Column(Time, nullable=False)
    __table_args__ = (
        CheckConstraint('hora_entrada < hora_salida', name='chk_tiempo_horas'),
        CheckConstraint('hora_entrada >= \'08:00:00\'', name='chk_entrada'),
        CheckConstraint('hora_salida <= \'22:00:00\'', name='chk_salida')
    )

class PersonalAdministrativo(Base):
    __tablename__ = 'personal_administrativo'
    dni = Column(String(8), ForeignKey('empleado.dni'), primary_key=True, nullable=False)
    salario = Column(DECIMAL(10, 2), nullable=False)
    __table_args__ = (
        CheckConstraint('salario >= 1025', name='chk_pa_salario'),
        UniqueConstraint('dni', name='dni_pa_unique')
    )

class Pago(Base):
    __tablename__ = 'pago'
    codigo = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    empleado_dni = Column(String(8), ForeignKey('empleado.dni'), nullable=False)
    fecha = Column(Date, nullable=False)
    monto = Column(DECIMAL(10, 2), nullable=False)
    __table_args__ = (
        CheckConstraint('monto > 0', name='pago_codigo_value'),
        CheckConstraint('fecha <= CURRENT_DATE', name='pago_fecha'),
        UniqueConstraint('codigo', name='codigo_pago_unique')
    )

class Deposito(Base):
    __tablename__ = 'deposito'
    pago_codigo = Column(Integer, ForeignKey('pago.codigo'), primary_key=True, nullable=False)
    administrativo_dni = Column(String(8), ForeignKey('personal_administrativo.dni'), nullable=False)
    __table_args__ = (
        UniqueConstraint('pago_codigo', name='codigo_dp_unique')
    )

class Ubicacion(Base):
    __tablename__ = 'ubicacion'
    codigo = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    direccion = Column(String, nullable=False)
    estado_provincia = Column(String, nullable=False)
    pais = Column(String, nullable=False)
    codigo_postal = Column(String, nullable=False)
    __table_args__ = (
        UniqueConstraint('codigo', name='codigo_ubi_unique')
    )

class Cliente(Base):
    __tablename__ = 'cliente'
    rin = Column(String(7), primary_key=True, nullable=False)
    nombre = Column(String, nullable=False)
    pais = Column(String, nullable=False)
    ubicacion_codigo = Column(Integer, ForeignKey('ubicacion.codigo'), nullable=False)
    __table_args__ = (
        UniqueConstraint('rin', name='rin_cliente_unique')
    )

class Pedido(Base):
    __tablename__ = 'pedido'
    po = Column(String(20), primary_key=True, nullable=False)
    fecha_pedido = Column(Date, nullable=False)
    fecha_entrega_propuesta = Column(Date, nullable=False)
    fecha_entrega = Column(Date)
    cliente_rin = Column(String(7), ForeignKey('cliente.rin'), nullable=False)
    __table_args__ = (
        CheckConstraint('po ILIKE \'PO%\'', name='pedido_po'),
        CheckConstraint('fecha_pedido < fecha_entrega_propuesta AND fecha_pedido < fecha_entrega', name='chk_pedido_fechas')
    )

class Supervisa(Base):
    __tablename__ = 'supervisa'
    administrativo_dni = Column(String(8), ForeignKey('personal_administrativo.dni'), primary_key=True, nullable=False)
    pedido_po = Column(String(20), ForeignKey('pedido.po'), primary_key=True, nullable=False)

class Empresa(Base):
    __tablename__ = 'empresa'
    ruc = Column(String(11), primary_key=True, nullable=False)
    ubicacion_facturacion_codigo = Column(Integer, ForeignKey('ubicacion.codigo'), nullable=False)
    ubicacion_codigo = Column(Integer, ForeignKey('ubicacion.codigo'), nullable=False)
    __table_args__ = (
        UniqueConstraint('ruc', name='ruc_empresa_unique')
    )

class Etapa(Base):
    __tablename__ = 'etapa'
    pedido_po = Column(String(20), ForeignKey('pedido.po'), primary_key=True, nullable=False)
    estado = Column(String(20), primary_key=True, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_finalizacion = Column(Date)
    empresa_ruc = Column(String(11), ForeignKey('empresa.ruc'), nullable=False)
    __table_args__ = (
        CheckConstraint("estado IN ('Compra hilo', 'Tejeduria', 'Tenido', 'Corte', 'Confeccion', 'Acabados', 'Listo para despacho', 'Despachado')", name='chk_etapa_estado')
    )

class Trabaja(Base):
    __tablename__ = 'trabaja'
    etapa_po = Column(String(20), primary_key=True, nullable=False)
    etapa_estado = Column(String(20), primary_key=True, nullable=False)
    trabajador_dni = Column(String(8), ForeignKey('trabajador_taller.dni'), primary_key=True, nullable=False)
    __table_args__ = (
        ForeignKeyConstraint(['etapa_po', 'etapa_estado'], ['etapa.pedido_po', 'etapa.estado'], name='fk_tte_etapa')
    )

class GuiaDeRemision(Base):
    __tablename__ = 'guia_de_remision'
    numero = Column(String(6), primary_key=True, nullable=False)
    tipo = Column(String(4), nullable=False)
    fecha = Column(Date, nullable=False)
    descripcion = Column(String, nullable=False)
    placa_vehiculo = Column(String, nullable=False)
    ubicacion_salida_codigo = Column(Integer, ForeignKey('ubicacion.codigo'), nullable=False)
    ubicacion_destino_codigo = Column(Integer, ForeignKey('ubicacion.codigo'), nullable=False)
    __table_args__ = (
        UniqueConstraint('numero', name='numero_guia_unique'),
        CheckConstraint("tipo IN ('T001', 'T002', 'T003', 'T004')", name='guia_tipo')
    )

class Factura(Base):
    __tablename__ = 'factura'
    numero = Column(String(6), primary_key=True, nullable=False)
    monto = Column(DECIMAL(10, 2), nullable=False)
    igv = Column(DECIMAL(10, 2), nullable=False)
    descripcion = Column(String, nullable=False)
    empresa_ruc = Column(String(11), ForeignKey('empresa.ruc'), nullable=False)
    ubicacion_codigo = Column(Integer, ForeignKey('ubicacion.codigo'), nullable=False)
    administrativo_dni = Column(String(8), ForeignKey('personal_administrativo.dni'), nullable=False)
    guia_numero = Column(String, ForeignKey('guia_de_remision.numero'), nullable=False)
    __table_args__ = (
        CheckConstraint('igv > 0', name='factura_igv'),
        UniqueConstraint('numero', name='numero_factura_unique')
    )

class Contiene(Base):
    __tablename__ = 'contiene'
    factura_numero = Column(String(6), ForeignKey('factura.numero'), primary_key=True, nullable=False)
    guia_numero = Column(String(6), ForeignKey('guia_de_remision.numero'), primary_key=True, nullable=False)

class Prenda(Base):
    __tablename__ = 'prenda'
    pedido_po = Column(String(20), ForeignKey('pedido.po'), primary_key=True, nullable=False)
    color = Column(String(20), primary_key=True, nullable=False)
    estilo = Column(String(20), primary_key=True, nullable=False)
    categoria = Column(String(10), nullable=False)
    __table_args__ = (
        CheckConstraint("categoria IN ('Damas', 'Caballeros', 'Ninos')", name='chk_prenda_categoria')
    )

class Polo(Base):
    __tablename__ = 'polo'
    prenda_po = Column(String(20), primary_key=True, nullable=False)
    prenda_color = Column(String(20), primary_key=True, nullable=False)
    prenda_estilo = Column(String(20), primary_key=True, nullable=False)
    tipo = Column(String(2), nullable=False)
    __table_args__ = (
        ForeignKeyConstraint(['prenda_po', 'prenda_color', 'prenda_estilo'], ['prenda.pedido_po', 'prenda.color', 'prenda.estilo'], name='fk_polo_prenda'),
        CheckConstraint("tipo IN ('LS', 'SS')", name='chk_polo_tipo')
    )

class Vestido(Base):
    __tablename__ = 'vestido'
    prenda_po = Column(String(20), primary_key=True, nullable=False)
    prenda_color = Column(String(20), primary_key=True, nullable=False)
    prenda_estilo = Column(String(20), primary_key=True, nullable=False)
    tipo = Column(String(12), nullable=False)
    __table_args__ = (
        ForeignKeyConstraint(['prenda_po', 'prenda_color', 'prenda_estilo'], ['prenda.pedido_po', 'prenda.color', 'prenda.estilo'], name='fk_vestido_prenda'),
        CheckConstraint("tipo IN ('Maxi', 'Skort', 'Short', 'Gaia', 'Imperial', 'A-line', 'Asymmetrical', 'Strapless', 'Column', 'Peplum', 'Sundress', 'Bouffant', 'Nightdress', 'Wrap', 'Bodycon', 'Halter', 'Sheath')", name='chk_vestido_tipo')
    )

class Talla(Base):
    __tablename__ = 'talla'
    prenda_po = Column(String(20), primary_key=True, nullable=False)
    prenda_color = Column(String(20), primary_key=True, nullable=False)
    prenda_estilo = Column(String(20), primary_key=True, nullable=False)
    upc = Column(String(12), primary_key=True, nullable=False)
    tamano = Column(String(3), nullable=False)
    precio = Column(DECIMAL(10, 2), nullable=False)
    cantidad = Column(Integer, nullable=False)
    __table_args__ = (
        ForeignKeyConstraint(['prenda_po', 'prenda_color', 'prenda_estilo'], ['prenda.pedido_po', 'prenda.color', 'prenda.estilo'], name='fk_talla_prenda'),
        CheckConstraint("tamano IN ('XXS', 'XS', 'S','M','L','XL','XXL','3XL')", name='chk_tamano'),
        CheckConstraint("cantidad > 0", name='chk_cantidad')
    )