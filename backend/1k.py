import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta, date
import calendar

fake = Faker()

# Create Faker instances for specific countries
fake_us = Faker('en_US')
fake_ca = Faker('en_CA')
fake_au = Faker('en_AU')
fake_in = Faker('en_IN')
fake_uk = Faker('en_GB')
fake_de = Faker('de_DE')
fake_fr = Faker('fr_FR')
fake_br = Faker('pt_BR')
fake_cn = Faker('zh_CN')
fake_mx = Faker('es_MX')
fake_pe = Faker('es_ES')  # Use es_ES for generating Peruvian data
fake_ar = Faker('es_AR')
fake_it = Faker('it_IT')
fake_es = Faker('es_ES')
fake_jp = Faker('ja_JP')
fake_ru = Faker('ru_RU')
fake_za = Faker('en_GB')  # Use en_GB for generating South African data
fake_eg = Faker('ar_EG')

fake_generics = Faker()

# Dictionary of countries and their states/provinces
country_states = {
    "USA": ["California", "Texas", "New York", "Florida", "Illinois", "Pennsylvania", "Ohio", "Georgia", "North Carolina", "Michigan"],
    "Canada": ["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba", "Saskatchewan", "Nova Scotia", "New Brunswick", "Newfoundland and Labrador", "Prince Edward Island"],
    "Australia": ["New South Wales", "Victoria", "Queensland", "Western Australia", "South Australia", "Tasmania", "Northern Territory", "Australian Capital Territory"],
    "India": ["Maharashtra", "Tamil Nadu", "Karnataka", "Gujarat", "Uttar Pradesh", "Rajasthan", "Madhya Pradesh", "West Bengal", "Bihar", "Punjab"],
    "UK": ["England", "Scotland", "Wales", "Northern Ireland"],
    "Germany": ["Bavaria", "North Rhine-Westphalia", "Baden-Württemberg", "Lower Saxony", "Hesse", "Saxony", "Rhineland-Palatinate", "Thuringia", "Saxony-Anhalt", "Brandenburg"],
    "France": ["Île-de-France", "Provence-Alpes-Côte d'Azur", "Auvergne-Rhône-Alpes", "Nouvelle-Aquitaine", "Occitanie", "Hauts-de-France", "Grand Est", "Brittany", "Normandy", "Bourgogne-Franche-Comté"],
    "Brazil": ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Bahia", "Paraná", "Rio Grande do Sul", "Pernambuco", "Ceará", "Pará", "Amazonas"],
    "China": ["Guangdong", "Shandong", "Henan", "Sichuan", "Jiangsu", "Hebei", "Hunan", "Anhui", "Hubei", "Zhejiang"],
    "Mexico": ["Ciudad de México", "Estado de México", "Jalisco", "Veracruz", "Puebla", "Guanajuato", "Nuevo León", "Chiapas", "Michoacán", "Oaxaca"],
    "Peru": ["Lima", "Arequipa", "Cusco", "Trujillo", "Chiclayo", "Piura", "Iquitos", "Tacna", "Puno", "Huancayo"],
    "Argentina": ["Buenos Aires", "Córdoba", "Santa Fe", "Mendoza", "Tucumán", "Entre Ríos", "Salta", "Misiones", "Chaco", "Corrientes"],
    "Italy": ["Lombardy", "Lazio", "Campania", "Sicily", "Veneto", "Piedmont", "Emilia-Romagna", "Tuscany", "Liguria", "Marche"],
    "Spain": ["Madrid", "Catalonia", "Andalusia", "Valencia", "Galicia", "Castile and León", "Basque Country", "Canary Islands", "Aragon", "Extremadura"],
    "Japan": ["Tokyo", "Osaka", "Kyoto", "Hokkaido", "Fukuoka", "Aichi", "Kanagawa", "Hyogo", "Chiba", "Shizuoka"],
    "Russia": ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Nizhny Novgorod", "Samara", "Omsk", "Kazan", "Chelyabinsk", "Rostov-on-Don"],
    "South Africa": ["Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape", "Mpumalanga", "Limpopo", "North West", "Free State", "Northern Cape"],
    "Egypt": ["Cairo", "Alexandria", "Giza", "Shubra El Kheima", "Port Said", "Suez", "Mansoura", "Tanta", "Asyut", "Ismailia"]
}

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="prueba_diana",
    user="postgres",
    password="123"
)
cur = conn.cursor()

# Schemas to populate
schemas = ["1k"]  # Add more schemas if needed


# Colors array
colors = [
    "Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Pink", "Brown", "Gray", "Black",
    "White", "Cyan", "Magenta", "Lime", "Maroon", "Navy", "Olive", "Teal", "Aqua", "Silver",
    "Gold", "Coral", "Salmon", "Hot Pink", "Lavender", "Indigo", "Ivory", "Beige", "Peach", "Mint",
    "Crimson", "Turquoise", "Violet", "Fuchsia", "Khaki", "Plum", "Periwinkle", "Orchid", "Amber", "Chocolate",
    "Chartreuse", "Azure", "Lilac", "Sapphire", "Ruby", "Emerald", "Topaz", "Opal", "Amethyst", "Rose",
    "Jade", "Pearl", "Quartz", "Burgundy", "Rust", "Sand", "Mustard", "Slate", "Tangerine", "Cinnamon",
    "Ginger", "Clay", "Copper", "Brass", "Bronze", "Blush", "Eggplant", "Mauve", "Forest Green", "Sea Green",
    "Sky Blue", "Cerulean", "Midnight Blue", "Powder Blue", "Mint Green", "Army Green", "Lemon", "Apricot",
    "Canary", "Flamingo", "Ivory", "Sienna", "Denim", "Almond", "Cobalt", "Honey", "Linen", "Moss",
    "Wheat", "Snow", "Tan", "Bisque", "Papaya", "Ocher", "Celadon", "Chestnut", "Saffron", "Brick Red"
]


for schema in schemas:
    # Generate data for 'empleado'

    def insert_in_batches(cursor, schema, batch):
        try:
            cursor.executemany("""
                INSERT INTO tiempo (fecha, dni, hora_entrada, hora_salida)
                VALUES (%s, %s, %s, %s)
            """, batch)
            conn.commit()
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print(f"Batch insertion failed: {e}")

    # Generate employees
    empleados = []
    for _ in range(500):  # Adjust number of employees as needed
        dni = fake.unique.numerify(text='########')
        nombres = fake.first_name()
        apellidos = fake.last_name()
        fecha_contratacion = fake.date_between(
            start_date='-1y', end_date='today')
        fecha_nacimiento = fake.date_between(
            start_date='-60y', end_date='-18y')
        empleados.append(
            (dni, nombres, apellidos, fecha_contratacion, fecha_nacimiento))

    cur.executemany("""
        INSERT INTO empleado (dni, nombres, apellidos, fecha_contratacion, fecha_nacimiento)
        VALUES (%s, %s, %s, %s, %s)
    """, empleados)
    conn.commit()
    print('empleados ready')

    # Select 3 to 10 employees to be 'personal_administrativo'
    num_admin = random.randint(30, 50)
    personal_administrativo = random.sample(empleados, num_admin)
    personal_administrativo = [(emp[0], round(random.uniform(
        1025, 5000), 2)) for emp in personal_administrativo]

    cur.executemany("""
        INSERT INTO personal_administrativo (dni, salario)
        VALUES (%s, %s)
    """, personal_administrativo)
    conn.commit()
    print('administrativos ready')

    # The remaining employees are 'trabajador_taller'
    trabajador_taller = [emp for emp in empleados if emp[0]
                         not in [pa[0] for pa in personal_administrativo]]
    trabajador_taller = [(emp[0], round(random.uniform(12, 15), 2))
                         for emp in trabajador_taller]

    cur.executemany("""
        INSERT INTO trabajador_taller (dni, tarifa)
        VALUES (%s, %s)
    """, trabajador_taller)
    conn.commit()
    print('trabajadores ready')

    def insert_in_batches(cursor, schema, batch):
        try:
            cursor.executemany("""
                INSERT INTO tiempo (fecha, dni, hora_entrada, hora_salida)
                VALUES (%s, %s, %s, %s)
            """, batch)
            conn.commit()
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print(f"Batch insertion failed: {e}")

    tiempos = []
    batch_size = 100  # Set the desired batch size

    for tt in trabajador_taller:
        dni = tt[0]
        fecha_contratacion = [emp[3] for emp in empleados if emp[0] == dni][0]
        current_date = datetime.now().date()

        for day in range((current_date - fecha_contratacion).days + 1):
            fecha = fecha_contratacion + timedelta(days=day)
            if fecha.weekday() < 5:  # Ensure the date is a weekday (Monday to Friday)
                start_entrada = datetime.strptime('08:00:00', '%H:%M:%S')
                end_entrada = datetime.strptime('18:00:00', '%H:%M:%S')
                delta_entrada = end_entrada - start_entrada

                if delta_entrada.total_seconds() > 0:
                    segundos_entrada = fake.random_int(
                        min=0, max=int(delta_entrada.total_seconds()))
                    hora_entrada = (
                        start_entrada + timedelta(seconds=segundos_entrada)).time()
                else:
                    hora_entrada = start_entrada.time()

                min_salida_time = datetime.combine(
                    fecha, hora_entrada) + timedelta(hours=4)
                max_salida_time = datetime.combine(
                    fecha, datetime.strptime('22:00:00', '%H:%M:%S').time())

                if min_salida_time > max_salida_time:
                    hora_salida = max_salida_time.time()
                else:
                    delta_salida = max_salida_time - min_salida_time
                    if delta_salida.total_seconds() > timedelta(hours=4).total_seconds():
                        segundos_salida = fake.random_int(
                            min=int(timedelta(hours=4).total_seconds()), max=int(delta_salida.total_seconds()))
                        hora_salida = (
                            min_salida_time + timedelta(seconds=segundos_salida)).time()
                    else:
                        hora_salida = min_salida_time.time()

                tiempos.append((fecha, dni, hora_entrada.strftime(
                    '%H:%M:%S'), hora_salida.strftime('%H:%M:%S')))

                if len(tiempos) >= batch_size:
                    insert_in_batches(cur, schema, tiempos)
                    tiempos = []

    # Insert any remaining records
    if tiempos:
        insert_in_batches(cur, schema, tiempos)
    print('tiempos ready')

    for admin in personal_administrativo:
        dni, monthly_salary = admin
        pay_date = datetime.now().replace(day=1)  # Payment on the first of each month
        for _ in range(12):  # Assume payments for one year
            cur.execute("""INSERT INTO pago (empleado_dni, fecha, monto) VALUES (%s, %s, %s)""",
                        (dni, pay_date, monthly_salary))
            # Go to the first of the previous month
            pay_date -= timedelta(days=30)

    # For trabajador de taller
    for worker in trabajador_taller:
        dni, rate = worker
        current_date = datetime.now()
        while current_date.weekday() != 5:
            current_date -= timedelta(days=1)  # Find the most recent Saturday
        for _ in range(52):  # Assume weekly payments for one year
            weekly_hours = sum(
                (datetime.strptime(end, '%H:%M:%S') -
                 datetime.strptime(start, '%H:%M:%S')).seconds / 3600
                for fecha, emp_dni, start, end in tiempos
                if emp_dni == dni and fecha == current_date.date()
            )
            payment = weekly_hours * rate
            if payment > 0:
                cur.execute(
                    """INSERT INTO pago (empleado_dni, fecha, monto) VALUES (%s, %s, %s)""",
                    (dni, current_date, payment))
            current_date -= timedelta(days=7)

    conn.commit()

    # Function to generate monthly payments for personal administrativo

    def generate_monthly_payments():
        cur.execute(
            """SELECT dni, salario FROM personal_administrativo""")
        for dni, salario in cur.fetchall():
            # Payment date is the first of each month, for the previous month
            for month in range(1, 13):
                last_day_of_month = calendar.monthrange(
                    datetime.now().year, month)[1]
                payment_date = date(datetime.now().year,
                                    month, last_day_of_month)
                if payment_date <= datetime.now().date():
                    cur.execute("""
                        INSERT INTO pago (empleado_dni, fecha, monto)
                        VALUES (%s, %s, %s)""",
                                (dni, payment_date, salario))
        conn.commit()

    # Function to generate weekly payments for trabajador de taller
    def generate_weekly_payments():
        cur.execute(
            """SELECT dni, tarifa FROM trabajador_taller""")
        for dni, tarifa in cur.fetchall():
            # Calculate weekly payment based on the current week's Monday to Friday
            today = datetime.now().date()
            last_monday = today - timedelta(days=today.weekday())
            last_friday = last_monday + timedelta(days=4)
            for week in range(52):
                week_start = last_monday - timedelta(weeks=week)
                week_end = last_friday - timedelta(weeks=week)
                cur.execute("""
                    SELECT SUM(EXTRACT(epoch FROM (hora_salida - hora_entrada)) / 3600) AS total_hours
                    FROM tiempo
                    WHERE dni = %s AND fecha BETWEEN %s AND %s""",
                            (dni, week_start, week_end))
                total_hours = cur.fetchone()[0] or 0
                weekly_payment = round(total_hours * tarifa, 2)
                if weekly_payment > 0:
                    # Ensure payment date is not in the future
                    payment_date = week_end if week_end <= today else today
                    cur.execute("""
                        INSERT INTO pago (empleado_dni, fecha, monto)
                        VALUES (%s, %s, %s)""",
                                (dni, payment_date, weekly_payment))
        conn.commit()

    # Invoke payment generation functions
    generate_monthly_payments()
    generate_weekly_payments()

    print('pagos ready')

    # Generate data for 'ubicacion'
    ubicaciones = []
    for _ in range(1500):  # Adjust number of locations as needed
        pais = random.choice(list(country_states.keys()))
        estado_provincia = random.choice(country_states[pais])
        if pais == "USA":
            direccion = fake_us.address()
            codigo_postal = fake_us.zipcode()
        elif pais == "Canada":
            direccion = fake_ca.address()
            codigo_postal = fake_ca.postcode()
        elif pais == "Australia":
            direccion = fake_au.address()
            codigo_postal = fake_au.postcode()
        elif pais == "India":
            direccion = fake_in.address()
            codigo_postal = fake_in.postcode()
        elif pais == "UK":
            direccion = fake_uk.address()
            codigo_postal = fake_uk.postcode()
        elif pais == "Germany":
            direccion = fake_de.address()
            codigo_postal = fake_de.postcode()
        elif pais == "France":
            direccion = fake_fr.address()
            codigo_postal = fake_fr.postcode()
        elif pais == "Brazil":
            direccion = fake_br.address()
            codigo_postal = fake_br.postcode()
        elif pais == "China":
            direccion = fake_cn.address()
            codigo_postal = fake_cn.postcode()
        elif pais == "Mexico":
            direccion = fake_mx.address()
            codigo_postal = fake_mx.postcode()
        elif pais == "Peru":
            direccion = fake_pe.address()
            codigo_postal = fake_pe.postcode()
        elif pais == "Argentina":
            direccion = fake_ar.address()
            codigo_postal = fake_ar.postcode()
        elif pais == "Italy":
            direccion = fake_it.address()
            codigo_postal = fake_it.postcode()
        elif pais == "Spain":
            direccion = fake_es.address()
            codigo_postal = fake_es.postcode()
        elif pais == "Japan":
            direccion = fake_jp.address()
            codigo_postal = fake_jp.postcode()
        elif pais == "Russia":
            direccion = fake_ru.address()
            codigo_postal = fake_ru.postcode()
        elif pais == "South Africa":
            direccion = fake_za.address()
            codigo_postal = fake_za.postcode()
        elif pais == "Egypt":
            direccion = fake_eg.address()
            codigo_postal = fake_eg.postcode()
        else:
            direccion = fake_generics.address()
            codigo_postal = fake_generics.postcode()
        ubicaciones.append((direccion, estado_provincia, pais, codigo_postal))

    cur.executemany("""
        INSERT INTO ubicacion (direccion, estado_provincia, pais, codigo_postal)
        VALUES (%s, %s, %s, %s)
    """, ubicaciones)
    conn.commit()
    print('ubicaciones ready')

    # Generate data for 'empresa'
    empresas = []
    for _ in range(500):  # Adjust number of companies as needed
        ruc = fake.unique.numerify(text='###########')
        ubicacion_facturacion_codigo = random.randint(1, 500)
        ubicacion_codigo = random.randint(1, 500)
        while True:
            # Ensure both locations are in the same country
            ubicacion_facturacion = ubicaciones[ubicacion_facturacion_codigo - 1]
            ubicacion_destino = ubicaciones[ubicacion_codigo - 1]
            if ubicacion_facturacion[2] == ubicacion_destino[2]:
                break
            ubicacion_codigo = random.randint(1, 500)
        empresas.append((ruc, ubicacion_facturacion_codigo, ubicacion_codigo))

    cur.executemany("""
        INSERT INTO empresa (ruc, ubicacion_facturacion_codigo, ubicacion_codigo)
        VALUES (%s, %s, %s)
    """, empresas)
    conn.commit()
    print('empresas ready')

    # Generate data for 'cliente'
    # Fetch ubicacion codes and countries
    cur.execute('SELECT codigo, pais FROM ubicacion')
    ubicacion_data = cur.fetchall()

    # Generate cliente records ensuring ubicacion_codigo matches pais
    clientes = []
    for _ in range(1000):  # Adjust number of clients as needed
        rin = fake.unique.bothify(text='??#####')
        nombre = fake.company()
        ubicacion = random.choice(ubicacion_data)
        ubicacion_codigo = ubicacion[0]
        pais = ubicacion[1]
        clientes.append((rin, nombre, pais, ubicacion_codigo))

    cur.executemany("""
        INSERT INTO cliente (rin, nombre, pais, ubicacion_codigo)
        VALUES (%s, %s, %s, %s)
    """, clientes)
    conn.commit()
    print('clientes ready')

    # Generate pedidos ensuring cliente_rin exists
    cur.execute('SELECT rin FROM cliente')
    cliente_rins = [row[0] for row in cur.fetchall()]

    # Generate data for 'pedido'
    pedidos = []
    for _ in range(1000):  # Adjust number of pedidos as needed
        po = fake.unique.bothify(text='PO########')
        fecha_pedido = fake.date_between(start_date='-10y', end_date='today')
        fecha_entrega_propuesta = fecha_pedido + \
            timedelta(days=random.randint(1, 30))
        fecha_entrega = fecha_entrega_propuesta + \
            timedelta(days=random.randint(0, 10))
        cliente_rin = random.choice(cliente_rins)
        pedidos.append(
            (po, fecha_pedido, fecha_entrega_propuesta, fecha_entrega, cliente_rin))

    cur.executemany("""
        INSERT INTO pedido (po, fecha_pedido, fecha_entrega_propuesta, fecha_entrega, cliente_rin)
        VALUES (%s, %s, %s, %s, %s)
    """, pedidos)
    conn.commit()
    print('pedidos ready')

    # Generate data for 'supervisa'
    supervisa = []
    for pedido in pedidos:
        administrativo_dni = random.choice(personal_administrativo)[0]
        supervisa.append((administrativo_dni, pedido[0]))

    cur.executemany("""
        INSERT INTO supervisa (administrativo_dni, pedido_po)
        VALUES (%s, %s)
    """, supervisa)
    conn.commit()
    print('supervisa ready')

    # Generate etapa records for each pedido
    etapas = []
    estados = ['Compra hilo', 'Tejeduria', 'Tenido', 'Corte',
               'Confeccion', 'Acabados', 'Listo para despacho', 'Despachado']
    empresas_ruc = [empresa[0] for empresa in empresas]

    for pedido in pedidos:
        fecha_inicio = fake.date_between(
            start_date=pedido[1], end_date=pedido[1] + timedelta(days=10))
        for estado in estados:
            fecha_finalizacion = None
            if random.choice([True, False]):
                fecha_finalizacion = fake.date_between(
                    start_date=fecha_inicio, end_date=fecha_inicio + timedelta(days=5))
            empresa_ruc = random.choice(empresas_ruc)
            etapas.append((pedido[0], estado, fecha_inicio,
                          fecha_finalizacion, empresa_ruc))
            if fecha_finalizacion:
                fecha_inicio = fecha_finalizacion + timedelta(days=1)
            else:
                break  # Stop generating further stages if the current one is not finished

    cur.executemany("""
        INSERT INTO etapa (pedido_po, estado, fecha_inicio, fecha_finalizacion, empresa_ruc)
        VALUES (%s, %s, %s, %s, %s)
    """, etapas)
    conn.commit()
    print('etapas ready')

    # Generate data for 'trabaja'
    cur.execute('SELECT pedido_po, estado FROM etapa')
    etapas_data = cur.fetchall()

    cur.execute('SELECT dni FROM trabajador_taller')
    trabajador_dnis = [row[0] for row in cur.fetchall()]

    trabaja = []
    for etapa in etapas_data:
        # Assign between 1 and 5 workers to each stage
        num_trabajadores = random.randint(1, 5)
        trabajadores_asignados = random.sample(
            trabajador_dnis, num_trabajadores)
        for trabajador_dni in trabajadores_asignados:
            trabaja.append((etapa[0], etapa[1], trabajador_dni))

    cur.executemany("""
        INSERT INTO trabaja (etapa_po, etapa_estado, trabajador_dni)
        VALUES (%s, %s, %s)
    """, trabaja)
    conn.commit()
    print('trabaja ready')

    # Generate data for 'guia_de_remision'
    guias = []
    for _ in range(100):  # Adjust number of guides as needed
        numero = fake.unique.numerify(text='######')
        tipo = random.choice(['T001', 'T002', 'T003', 'T004'])
        fecha = fake.date_between(start_date='-10y', end_date='today')
        descripcion = fake.text()
        pais = random.choice(list(country_states.keys()))

        if pais == "USA":
            placa_vehiculo = fake_us.license_plate()
        elif pais == "Canada":
            placa_vehiculo = fake_ca.license_plate()
        elif pais == "Australia":
            placa_vehiculo = fake_au.license_plate()
        elif pais == "India":
            placa_vehiculo = fake_in.license_plate()
        elif pais == "UK":
            placa_vehiculo = fake_uk.license_plate()
        elif pais == "Germany":
            placa_vehiculo = fake_de.license_plate()
        elif pais == "France":
            placa_vehiculo = fake_fr.license_plate()
        elif pais == "Brazil":
            placa_vehiculo = fake_br.license_plate()
        elif pais == "China":
            placa_vehiculo = fake_cn.license_plate()
        elif pais == "Mexico":
            placa_vehiculo = fake_mx.license_plate()
        elif pais == "Peru":
            placa_vehiculo = fake_pe.license_plate()
        elif pais == "Argentina":
            placa_vehiculo = fake_ar.license_plate()
        elif pais == "Italy":
            placa_vehiculo = fake_it.license_plate()
        elif pais == "Spain":
            placa_vehiculo = fake_es.license_plate()
        elif pais == "Japan":
            placa_vehiculo = fake_jp.license_plate()
        elif pais == "Russia":
            placa_vehiculo = fake_ru.license_plate()
        elif pais == "South Africa":
            placa_vehiculo = fake_za.license_plate()
        elif pais == "Egypt":
            placa_vehiculo = fake_eg.license_plate()
        else:
            placa_vehiculo = fake_generics.license_plate()

        ubicacion_salida_codigo = random.randint(1, 500)
        ubicacion_destino_codigo = random.randint(1, 500)
        while True:
            # Ensure both locations are in the same country
            ubicacion_salida = ubicaciones[ubicacion_salida_codigo - 1]
            ubicacion_destino = ubicaciones[ubicacion_destino_codigo - 1]
            if ubicacion_salida[2] == ubicacion_destino[2]:
                break
            ubicacion_destino_codigo = random.randint(1, 500)
        guias.append((numero, tipo, fecha, descripcion, placa_vehiculo,
                      ubicacion_salida_codigo, ubicacion_destino_codigo))

    cur.executemany("""
        INSERT INTO guia_de_remision (numero, tipo, fecha, descripcion, placa_vehiculo, ubicacion_salida_codigo, ubicacion_destino_codigo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, guias)
    conn.commit()
    print('guias ready')

    # Generate data for 'factura'
    facturas = []
    for _ in range(100):  # Adjust number of invoices as needed
        numero = fake.unique.numerify(text='######')
        monto = round(random.uniform(100, 10000), 2)
        igv = round(monto * 0.18, 2)
        descripcion = fake.text()
        empresa = random.choice(empresas)
        empresa_ruc = empresa[0]
        # Corresponds to ubicacion_facturacion_codigo of the empresa
        ubicacion_factura_codigo = empresa[1]
        administrativo_dni = random.choice(personal_administrativo)[0]
        guia_numero = random.choice(guias)[0]
        facturas.append((numero, monto, igv, descripcion, empresa_ruc,
                        ubicacion_factura_codigo, administrativo_dni, guia_numero))

    cur.executemany("""
        INSERT INTO factura (numero, monto, igv, descripcion, empresa_ruc, ubicacion_codigo, administrativo_dni, guia_numero)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, facturas)
    conn.commit()
    print('facturas ready')

    # Generate data for 'contiene'
    factura_guia = []
    for factura in facturas:
        factura_guia.append((factura[0], factura[7]))

    cur.executemany("""
        INSERT INTO contiene (factura_numero, guia_numero)
        VALUES (%s, %s)
    """, factura_guia)
    conn.commit()
    print('contiene ready')

    # Generate data for 'prenda'
    prendas = []
    estilos = ['Formal', 'Casual', 'Deportivo']
    categorias = ['Damas', 'Caballeros', 'Ninos']

    cur.execute('SELECT po FROM pedido')
    pedido_pos = [row[0] for row in cur.fetchall()]
    prendas = set()
    prendas_to_insert = []

    for pedido_po in pedido_pos:
        num_prendas = random.randint(1, 100)
        for _ in range(num_prendas):
            color = random.choice(colors)
            estilo = random.choice(estilos)
            categoria = random.choice(categorias)
            prenda = (pedido_po, color, estilo, categoria)
            if (pedido_po, color, estilo) not in prendas:
                prendas.add((pedido_po, color, estilo))
                prendas_to_insert.append(prenda)

    cur.executemany("""
        INSERT INTO prenda (pedido_po, color, estilo, categoria)
        VALUES (%s, %s, %s, %s)
    """, prendas_to_insert)
    conn.commit()
    print('prendas ready')

    # Generate data for 'polo'
    polos = []
    tipos_polo = ['LS', 'SS']
    for prenda in prendas:
        if random.choice([True, False]):  # Randomly assign some garments as 'polo'
            tipo = random.choice(tipos_polo)
            polos.append((prenda[0], prenda[1], prenda[2], tipo))

    cur.executemany("""
        INSERT INTO polo (prenda_po, prenda_color, prenda_estilo, tipo)
        VALUES (%s, %s, %s, %s)
    """, polos)
    conn.commit()
    print('polos ready')

    # Generate data for 'vestido'
    vestidos = []
    tipos_vestido = ['Maxi', 'Skort', 'Short', 'Gaia', 'Imperial', 'A-line', 'Asymmetrical', 'Strapless',
                     'Column', 'Peplum', 'Sundress', 'Bouffant', 'Nightdress', 'Wrap', 'Bodycon', 'Halter', 'Sheath']
    for prenda in prendas:
        if random.choice([True, False]):  # Randomly assign some garments as 'vestido'
            tipo = random.choice(tipos_vestido)
            vestidos.append((prenda[0], prenda[1], prenda[2], tipo))

    cur.executemany("""
        INSERT INTO vestido (prenda_po, prenda_color, prenda_estilo, tipo)
        VALUES (%s, %s, %s, %s)
    """, vestidos)
    conn.commit()
    print('vestidos ready')

    # Generate data for 'talla'
    tallas = []
    tamanos = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL']

    for prenda in prendas:
        num_tallas = random.randint(1, 8)  # Up to 8 different sizes
        selected_tamanos = sorted(random.sample(
            tamanos, num_tallas), key=tamanos.index)
        # Generate a random base price for the smallest size
        base_price = round(random.uniform(10, 20), 2)
        # Increment value for subsequent sizes
        increment = round(random.uniform(2, 10), 2)

        for i, tamano in enumerate(selected_tamanos):
            upc = fake.unique.numerify(text='############')
            # Increment price for each subsequent size
            precio = base_price + (i * increment)
            cantidad = random.randint(1, 100)
            tallas.append((prenda[0], prenda[1], prenda[2],
                           upc, tamano, round(precio, 2), cantidad))

    batch_size = 100  # Define the batch size
    total_batches = (len(tallas) + batch_size - 1) // batch_size

    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(tallas))
        batch = tallas[start_idx:end_idx]

        cur.executemany("""
        INSERT INTO talla (prenda_po, prenda_color, prenda_estilo, upc, tamano, precio, cantidad)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, batch)
        conn.commit()

    print('tallas ready')
    # Commit the changes to the database
    conn.commit()

# Close the connection
cur.close()
conn.close()
