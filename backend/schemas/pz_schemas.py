from pydantic import BaseModel, Field, field_validator
from datetime import date, time
from decimal import Decimal
from typing import Optional, List

class Empleado(BaseModel):
    dni: str = Field(..., max_length=8)
    nombres: str
    apellidos: str
    fecha_contratacion: date
    fecha_nacimiento: date

    class Config:
        from_attributes = True

class EmpleadoResponse(Empleado):
    pass

class TrabajadorTaller(BaseModel):
    dni: str = Field(..., max_length=8)
    tarifa: Decimal

    @field_validator('tarifa')
    def tarifa_rango(cls, value):
        if not (Decimal('12') <= value <= Decimal('15')):
            raise ValueError('La tarifa debe estar entre 12 y 15')
        return value

    class Config:
        from_attributes = True

class TrabajadorTallerResponse(TrabajadorTaller):
    pass

class Tiempo(BaseModel):
    fecha: date
    dni: str = Field(..., max_length=8)
    hora_entrada: time
    hora_salida: time

    @field_validator('hora_salida')
    def validar_horas(cls, hora_salida, values):
        if 'hora_entrada' in values and hora_salida <= values['hora_entrada']:
            raise ValueError('La hora de salida debe ser después de la hora de entrada')
        if hora_salida > time(22, 0, 0):
            raise ValueError('La hora de salida debe ser antes de las 22:00')
        return hora_salida

    @field_validator('hora_entrada')
    def validar_hora_entrada(cls, hora_entrada):
        if hora_entrada < time(8, 0, 0):
            raise ValueError('La hora de entrada debe ser después de las 08:00')
        return hora_entrada

    class Config:
        from_attributes = True

class TiempoResponse(Tiempo):
    pass

class PersonalAdministrativo(BaseModel):
    dni: str = Field(..., max_length=8)
    salario: Decimal

    @field_validator('salario')
    def salario_minimo(cls, value):
        if value < Decimal('1025'):
            raise ValueError('El salario debe ser al menos 1025')
        return value

    class Config:
        from_attributes = True

class PersonalAdministrativoResponse(PersonalAdministrativo):
    pass

class Pago(BaseModel):
    codigo: Optional[int] = None
    empleado_dni: str = Field(..., max_length=8)
    fecha: date
    monto: Decimal

    @field_validator('monto')
    def monto_positivo(cls, value):
        if value <= Decimal('0'):
            raise ValueError('El monto debe ser mayor a 0')
        return value

    @field_validator('fecha')
    def fecha_pasada(cls, value):
        if value > date.today():
            raise ValueError('La fecha debe ser igual o anterior a hoy')
        return value

    class Config:
        from_attributes = True

class PagoResponse(Pago):
    pass

class Deposito(BaseModel):
    pago_codigo: int
    administrativo_dni: str = Field(..., max_length=8)

    class Config:
        from_attributes = True

class DepositoResponse(Deposito):
    pass

class Ubicacion(BaseModel):
    codigo: Optional[int] = None
    direccion: str
    estado_provincia: str
    pais: str
    codigo_postal: str

    class Config:
        from_attributes = True

class UbicacionResponse(Ubicacion):
    pass

class Cliente(BaseModel):
    rin: str = Field(..., max_length=7)
    nombre: str
    pais: str
    ubicacion_codigo: int

    class Config:
        from_attributes = True

class ClienteResponse(Cliente):
    pass

class Pedido(BaseModel):
    po: str = Field(..., max_length=20)
    fecha_pedido: date
    fecha_entrega_propuesta: date
    fecha_entrega: Optional[date] = None
    cliente_rin: str = Field(..., max_length=7)

    @field_validator('fecha_entrega_propuesta', 'fecha_entrega', pre=True)
    def validar_fechas(cls, value, values, field):
        if 'fecha_pedido' in values and value is not None and value <= values['fecha_pedido']:
            raise ValueError(f'{field.name} debe ser posterior a fecha_pedido')
        return value

    class Config:
        from_attributes = True

class PedidoResponse(Pedido):
    pass

class Supervisa(BaseModel):
    administrativo_dni: str = Field(..., max_length=8)
    pedido_po: str = Field(..., max_length=20)

    class Config:
        from_attributes = True

class SupervisaResponse(Supervisa):
    pass

class Empresa(BaseModel):
    ruc: str = Field(..., max_length=11)
    ubicacion_facturacion_codigo: int
    ubicacion_codigo: int

    class Config:
        from_attributes = True

class EmpresaResponse(Empresa):
    pass

class Etapa(BaseModel):
    pedido_po: str = Field(..., max_length=20)
    estado: str = Field(..., max_length=20)
    fecha_inicio: date
    fecha_finalizacion: Optional[date] = None
    empresa_ruc: str = Field(..., max_length=11)

    @field_validator('estado')
    def estado_valido(cls, value):
        estados_validos = ['Compra hilo', 'Tejeduría', 'Teñido', 'Corte', 'Confección', 'Acabados', 'Listo para despacho', 'Despachado']
        if value not in estados_validos:
            raise ValueError(f'Estado debe ser uno de {estados_validos}')
        return value

    class Config:
        from_attributes = True

class EtapaResponse(Etapa):
    pass

class Trabaja(BaseModel):
    etapa_po: str = Field(..., max_length=20)
    etapa_estado: str = Field(..., max_length=20)
    trabajador_dni: str = Field(..., max_length=8)

    class Config:
        from_attributes = True

class TrabajaResponse(Trabaja):
    pass

class GuiaDeRemision(BaseModel):
    numero: str = Field(..., max_length=6)
    tipo: str = Field(..., max_length=4)
    fecha: date
    descripcion: str
    placa_vehiculo: str = Field(..., max_length=7)
    ubicacion_salida_codigo: int
    ubicacion_destino_codigo: int

    @field_validator('tipo')
    def tipo_valido(cls, value):
        tipos_validos = ['T001', 'T002', 'T003', 'T004']
        if value not in tipos_validos:
            raise ValueError(f'Tipo debe ser uno de {tipos_validos}')
        return value

    class Config:
        from_attributes = True

class GuiaDeRemisionResponse(GuiaDeRemision):
    pass

class Factura(BaseModel):
    numero: str = Field(..., max_length=6)
    monto: Decimal
    igv: Decimal
    descripcion: str
    empresa_ruc: str = Field(..., max_length=11)
    ubicacion_codigo: int
    administrativo_dni: str = Field(..., max_length=8)
    guia_numero: str = Field(..., max_length=6)

    @field_validator('igv')
    def igv_positivo(cls, value):
        if value <= Decimal('0'):
            raise ValueError('El IGV debe ser mayor a 0')
        return value

    class Config:
        from_attributes = True

class FacturaResponse(Factura):
    pass

class Contiene(BaseModel):
    factura_numero: str = Field(..., max_length=6)
    guia_numero: str = Field(..., max_length=6)

    class Config:
        from_attributes = True

class ContieneResponse(Contiene):
    pass

class Prenda(BaseModel):
    pedido_po: str = Field(..., max_length=20)
    color: str = Field(..., max_length=20)
    estilo: str

    class Config:
        from_attributes = True

class PrendaResponse(Prenda):
    pass

class Polo(BaseModel):
    pedido_po: str = Field(..., max_length=20)
    color: str = Field(..., max_length=20)
    talla: str = Field(..., max_length=4)

    @field_validator('talla')
    def talla_valida(cls, value):
        tallas_validas = ['XS', 'S', 'M', 'L', 'XL']
        if value not in tallas_validas:
            raise ValueError(f'Talla debe ser una de {tallas_validas}')
        return value

    class Config:
        from_attributes = True

class PoloResponse(Polo):
    pass

class Vestido(BaseModel):
    pedido_po: str = Field(..., max_length=20)
    color: str = Field(..., max_length=20)
    talla: str = Field(..., max_length=4)

    @field_validator('talla')
    def talla_valida(cls, value):
        tallas_validas = ['XS', 'S', 'M', 'L', 'XL']
        if value not in tallas_validas:
            raise ValueError(f'Talla debe ser una de {tallas_validas}')
        return value

    class Config:
        from_attributes = True

class VestidoResponse(Vestido):
    pass

class Talla(BaseModel):
    pedido_po: str = Field(..., max_length=20)
    color: str = Field(..., max_length=20)
    talla: str = Field(..., max_length=4)

    @field_validator('talla')
    def talla_valida(cls, value):
        tallas_validas = ['XS', 'S', 'M', 'L', 'XL']
        if value not in tallas_validas:
            raise ValueError(f'Talla debe ser una de {tallas_validas}')
        return value

    class Config:
        from_attributes = True

class TallaResponse(Talla):
    pass
