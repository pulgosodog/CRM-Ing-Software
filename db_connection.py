import sqlite3
import random
from datetime import datetime, timedelta

def conectar():
    """
    Crea y retorna una conexión a la base de datos 'crm_law_firm.db'.
    Si la base de datos no existe, SQLite la creará automáticamente.
    """
    try:
        print("Conexión exitosa a la base de datos")
        return sqlite3.connect('crm_law_firm.db')
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def cerrar_conexion(conexion):
    """
    Cierra la conexión activa a la base de datos.
    """
    if conexion:
        conexion.close()
        print("Conexión cerrada exitosamente")


def create_clientes_table(db_path="crm_law_firm.db"):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_completo TEXT NOT NULL,
            telefono TEXT,
            email TEXT UNIQUE,
            preferencias TEXT,
            fecha_nacimiento TEXT,
            estado_actividad TEXT DEFAULT 'Inactivo',
            notas TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_sample_clientes_data(db_path="crm_law_firm.db"):
    """
    Inserts sample data into the 'clientes' table.
    Args:
        db_path (str): Path to the SQLite database file.
    """
    
    sample_data = [
    ("Ricardo Pérez", "555-9876", "ricardo.perez@example.com", "Correo", "1982-02-14", "Activo", "Cliente leal desde 2015."),
    ("Carmen Silva", "555-1235", "carmen.silva@example.com", "SMS", "1993-07-11", "Inactivo", "Caso pendiente desde 2021."),
    ("Miguel Torres", "555-5432", "miguel.torres@example.com", "Llamadas", "1986-05-22", "Activo", "Prefiere contacto por teléfono."),
    ("Laura Gómez", "555-6543", "laura.gomez@example.com", "Correo", "1989-11-09", "Inactivo", "Última actividad registrada en 2020."),
    ("José Martínez", "555-8769", "jose.martinez@example.com", "SMS", "1977-03-18", "Activo", "Cliente regular con varios casos."),
    ("Vanessa Rodríguez", "555-2345", "vanessa.rodriguez@example.com", "Llamadas", "1994-01-30", "Activo", "Solicita reuniones periódicas."),
    ("Tomás Díaz", "555-9870", "tomas.diaz@example.com", "Correo", "1990-12-10", "Inactivo", "No tiene actividad desde 2019."),
    ("Raúl Sánchez", "555-6789", "raul.sanchez@example.com", "SMS", "1985-08-20", "Activo", "Cliente con varias consultas abiertas."),
    ("Paula López", "555-1358", "paula.lopez@example.com", "Correo", "1988-04-02", "Inactivo", "Última interacción en 2022."),
    ("Julio Fernández", "555-3597", "julio.fernandez@example.com", "Llamadas", "1984-06-30", "Activo", "Le gusta discutir todos los detalles."),
    ("Esteban Ruiz", "555-4502", "esteban.ruiz@example.com", "Correo", "1991-10-15", "Inactivo", "Cliente inactivo desde 2021."),
    ("Elena Jiménez", "555-6548", "elena.jimenez@example.com", "SMS", "1987-02-25", "Activo", "Está interesada en nuevos servicios."),
    ("Juan Pérez", "555-1234", "juan.perez@example.com", "Correo", "1985-02-15", "Activo", "Cliente regular desde 2020."),
    ("María López", "555-5678", "maria.lopez@example.com", "Llamadas", "1990-07-25", "Activo", "Prefiere llamadas por la tarde."),
    ("Carlos Martínez", "555-8765", "carlos.martinez@example.com", "SMS", "1988-11-05", "Inactivo", "Último caso cerrado en 2021."),
    ("Ana Gómez", "555-4321", "ana.gomez@example.com", "Correo", "1995-03-12", "Activo", "Cliente desde 2022."),
    ("Pedro Sánchez", "555-2468", "pedro.sanchez@example.com", "Correo", "1975-12-30", "Activo", "Tiene un caso pendiente."),
    ("Luisa Fernández", "555-1357", "luisa.fernandez@example.com", "Llamadas", "1980-06-18", "Inactivo", "No ha renovado su contrato."),
    ("Jorge Ramírez", "555-9753", "jorge.ramirez@example.com", "SMS", "1992-01-08", "Activo", "Requiere seguimiento mensual."),
    ("Sofía Torres", "555-8642", "sofia.torres@example.com", "Correo", "1987-10-14", "Inactivo", "Caso pendiente cerrado en 2020."),
    ]


    try:
        # Conexión a la base de datos
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Insertar datos
        cursor.executemany("""
        INSERT INTO clientes (nombre_completo, telefono, email, preferencias, fecha_nacimiento, estado_actividad, notas)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, sample_data)

        # Confirmar cambios
        connection.commit()
        print("Datos insertados con éxito en la tabla 'clientes'.")

    except sqlite3.Error as e:
        print(f"Error al insertar datos: {e}")

    finally:
        # Cerrar la conexión
        if connection:
            connection.close()

def fetch_and_display_clientes(db_path="crm_law_firm.db"):
    """
    Fetches and displays all data from the 'clientes' table.
    Args:
        db_path (str): Path to the SQLite database file.
    """
    try:
        # Conexión a la base de datos
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Recuperar datos de la tabla 'clientes'
        cursor.execute("SELECT * FROM clientes;")
        rows = cursor.fetchall()

        # Mostrar los datos en formato tabular
        print(f"{'ID':<5} {'Nombre Completo':<25} {'Teléfono':<15} {'Email':<30} {'Preferencias':<15} {'Nacimiento':<12} {'Estado':<10} {'Notas':<30}")
        print("=" * 140)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<25} {row[2]:<15} {row[3]:<30} {row[4]:<15} {row[5]:<12} {row[6]:<10} {row[7]:<30}")

    except sqlite3.Error as e:
        print(f"Error al recuperar datos: {e}")

    finally:
        # Cerrar la conexión
        if connection:
            connection.close()

def insertar_cliente(nombre_completo, telefono, email, preferencias, fecha_nacimiento, notas):
    """
    Inserta un cliente en la base de datos.
    """
    print("Intentando conectar a la base de datos...")  # Depuración
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")  # Depuración
        return False

    try:
        print("Conexión exitosa. Intentando insertar cliente...")  # Depuración
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre_completo, telefono, email, preferencias, fecha_nacimiento, notas)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre_completo, telefono, email, preferencias, fecha_nacimiento, notas))
        conexion.commit()
        print("Cliente agregado exitosamente.")  # Depuración
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error al agregar cliente: {e}")  # Depuración
        return False
    finally:
        cerrar_conexion(conexion)



def create_abogados_table(db_path="crm_law_firm.db"):
    conn = conectar()  # Usar la función que conecta a la base de datos
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS abogados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único del abogado
            nombre_completo TEXT NOT NULL,          -- Nombre completo del abogado
            correo TEXT,                            -- Correo electrónico del abogado
            especialidad TEXT,                      -- Especialidad del abogado (Civil, Penal, etc.)
            notas TEXT                              -- Notas adicionales sobre el abogado
        )
    """)
    conn.commit()  # Guardar los cambios en la base de datos
    conn.close()   # Cerrar la conexión con la base de datos

def insert_sample_abogados_data(db_path="crm_law_firm.db"):
    """
    Inserts sample data into the 'abogados' table.
    Args:
        db_path (str): Path to the SQLite database file.
    """
    
    sample_data = [
        ("Ricardo Pérez", "ricardo.perez@example.com", "Civil", "Abogado con más de 10 años de experiencia en derecho civil."),
        ("Carmen Silva", "carmen.silva@example.com", "Penal", "Especializada en derecho penal y litigios complejos."),
        ("Miguel Torres", "miguel.torres@example.com", "Laboral", "Abogado con amplia experiencia en defensa laboral y contratos."),
        ("Laura Gómez", "laura.gomez@example.com", "Familia", "Experta en derecho de familia y resolución de conflictos familiares."),
        ("José Martínez", "jose.martinez@example.com", "Comercial", "Especialista en derecho comercial y contratos corporativos."),
        ("Vanessa Rodríguez", "vanessa.rodriguez@example.com", "Mercantil", "Abogada especializada en derecho mercantil y fusiones."),
        ("Tomás Díaz", "tomas.diaz@example.com", "Propiedad intelectual", "Defiende derechos de propiedad intelectual y patentes."),
        ("Raúl Sánchez", "raul.sanchez@example.com", "Inmobiliario", "Abogado con experiencia en transacciones inmobiliarias y contratos de arrendamiento."),
        ("Paula López", "paula.lopez@example.com", "Corporativo", "Asesora a empresas en fusiones, adquisiciones y derecho corporativo."),
        ("Julio Fernández", "julio.fernandez@example.com", "Administrativo", "Experto en derecho administrativo y litigios con el estado."),
        ("Esteban Ruiz", "esteban.ruiz@example.com", "Tributario", "Abogado especializado en derecho tributario y planificación fiscal."),
        ("Elena Jiménez", "elena.jimenez@example.com", "Internacional", "Defiende a clientes en asuntos de derecho internacional y arbitraje."),
    ]

    try:
        # Conexión a la base de datos
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Insertar datos
        cursor.executemany("""
        INSERT INTO abogados (nombre_completo, correo, especialidad, notas)
        VALUES (?, ?, ?, ?);
        """, sample_data)

        # Confirmar cambios
        connection.commit()
        print("Datos insertados con éxito en la tabla 'abogados'.")

    except sqlite3.Error as e:
        print(f"Error al insertar datos: {e}")

    finally:
        # Cerrar la conexión
        if connection:
            connection.close()

def fetch_and_display_abogados(db_path="crm_law_firm.db"):
    """
    Fetches and displays all data from the 'abogados' table.
    Args:
        db_path (str): Path to the SQLite database file.
    """
    try:
        # Conexión a la base de datos
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Recuperar datos de la tabla 'abogados'
        cursor.execute("SELECT * FROM abogados;")
        rows = cursor.fetchall()

        # Mostrar los datos en formato tabular
        print(f"{'ID':<5} {'Nombre Completo':<25} {'Correo':<30} {'Especialidad':<20} {'Notas':<50}")
        print("=" * 140)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<25} {row[2]:<30} {row[3]:<20} {row[4]:<50}")

    except sqlite3.Error as e:
        print(f"Error al recuperar datos: {e}")

    finally:
        # Cerrar la conexión
        if connection:
            connection.close()


def create_asistentes_table(db_path="crm_law_firm.db"):
    """
    Crea la tabla 'asistentes' si no existe.
    """
    conn = sqlite3.connect(db_path)  # Usar la función que conecta a la base de datos
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asistentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único del asistente
            nombre_completo TEXT NOT NULL,          -- Nombre completo del asistente
            correo TEXT,                            -- Correo electrónico del asistente
            cargo TEXT,                             -- Cargo del asistente (todas comparten el mismo cargo por ahora)
            notas TEXT,                             -- Notas adicionales sobre el asistente
            estado_actividad BOOLEAN DEFAULT 1      -- Estado de actividad (1 = activo, 0 = inactivo)
        )
    """)
    conn.commit()  # Guardar los cambios en la base de datos
    conn.close()   # Cerrar la conexión con la base de datos

def insert_sample_asistentes_data(db_path="crm_law_firm.db"):
    """
    Inserta datos de ejemplo en la tabla 'asistentes'.
    Args:
        db_path (str): Ruta del archivo de la base de datos SQLite.
    """
    
    sample_data = [
        ('Juan Pérez', 'juan.perez@example.com', 'Asistente', 'Notas sobre Juan', 1),
        ('Ana Gómez', 'ana.gomez@example.com', 'Asistente', 'Notas sobre Ana', 1),
        ('Luis Rodríguez', 'luis.rodriguez@example.com', 'Asistente', 'Notas sobre Luis', 1),
        ('María López', 'maria.lopez@example.com', 'Asistente', 'Notas sobre María', 0),
        ('Carlos Martín', 'carlos.martin@example.com', 'Asistente', 'Notas sobre Carlos', 1),
        ('Lucía Fernández', 'lucia.fernandez@example.com', 'Asistente', 'Notas sobre Lucía', 1),
        ('Pedro García', 'pedro.garcia@example.com', 'Asistente', 'Notas sobre Pedro', 0),
        ('Sofía Torres', 'sofia.torres@example.com', 'Asistente', 'Notas sobre Sofía', 1),
        ('Diego Sánchez', 'diego.sanchez@example.com', 'Asistente', 'Notas sobre Diego', 1),
        ('Laura Díaz', 'laura.diaz@example.com', 'Asistente', 'Notas sobre Laura', 0),
        ('Felipe Romero', 'felipe.romero@example.com', 'Asistente', 'Notas sobre Felipe', 1),
        ('Elena Ruiz', 'elena.ruiz@example.com', 'Asistente', 'Notas sobre Elena', 0)
    ]
    
    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Insertar datos
        cursor.executemany("""
        INSERT INTO asistentes (nombre_completo, correo, cargo, notas, estado_actividad)
        VALUES (?, ?, ?, ?, ?);
        """, sample_data)

        # Confirmar cambios
        conn.commit()
        print("Datos insertados con éxito en la tabla 'asistentes'.")

    except sqlite3.Error as e:
        print(f"Error al insertar datos: {e}")

    finally:
        # Cerrar la conexión
        if conn:
            conn.close()


def create_casos_table(db_path="crm_law_firm.db"):
    conn = conectar()  # Usar la función que conecta a la base de datos
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE casos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    nombre_caso TEXT NOT NULL,
    tipo_caso TEXT NOT NULL,
    estado BOOLEAN NOT NULL DEFAULT 1, -- 1: Abierto, 0: Cerrado
    prioridad INTEGER NOT NULL DEFAULT 2, -- 1: Alta, 2: Media, 3: Baja
    id_abogado INTEGER,
    id_asistente INTEGER,
    fecha_creacion TEXT NOT NULL,
    fecha_deadline TEXT NOT NULL,
    id_documentos INTEGER,
    FOREIGN KEY (id_cliente) REFERENCES clientes (id),
    FOREIGN KEY (id_abogado) REFERENCES abogados (id),
    FOREIGN KEY (id_asistente) REFERENCES asistentes (id)
    ) 
    """)
    conn.commit()  # Guardar los cambios
    conn.close()  # Cerrar la conexión

def insert_sample_casos_data(db_path="crm_law_firm.db"):
    """
    Inserta datos de ejemplo en la tabla 'casos' con prioridad como número.
    """
    casos_data = []
    tipos_caso = ['Civil', 'Penal', 'Laboral', 'Familiar', 'Mercantil', 'Comercial']
    
    # Prioridad ahora es un número: 1 (Alta), 2 (Media), 3 (Baja)
    prioridades = [1, 2, 3]
    today = datetime.today()

    for _ in range(20):  # Crear 20 casos
        id_cliente = random.randint(1, 20)
        id_abogado = random.randint(1, 12)
        id_asistente = random.randint(1, 12)
        nombre_caso = f"Caso de {random.choice(tipos_caso)} {random.randint(1000, 9999)}"
        tipo_caso = random.choice(tipos_caso)
        estado = random.choice([0, 1])
        prioridad = random.choice(prioridades)
        fecha_creacion = today.strftime('%Y-%m-%d %H:%M:%S')
        fecha_deadline = (today + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')

        casos_data.append((
            id_cliente, nombre_caso, tipo_caso, estado, prioridad, 
            id_abogado, id_asistente, fecha_creacion, fecha_deadline, None
        ))

    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.executemany("""
        INSERT INTO casos (id_cliente, nombre_caso, tipo_caso, estado, prioridad, 
                           id_abogado, id_asistente, fecha_creacion, fecha_deadline, id_documentos)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, casos_data)

        connection.commit()
        print("Datos insertados con éxito en la tabla 'casos'.")
    except sqlite3.Error as e:
        print(f"Error al insertar datos en 'casos': {e}")
    finally:
        if connection:
            connection.close()            


def create_tickets_table(db_path="crm_law_firm.db"):
    """
    Crea la tabla 'tickets' si no existe.
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Crear la tabla 'tickets'
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asistente_id INTEGER,
            caso_id INTEGER,
            estado TEXT CHECK(estado IN ('abierto', 'cerrado')),
            nota TEXT,
            fecha_creacion TEXT,
            fecha_cierre TEXT,
            FOREIGN KEY (asistente_id) REFERENCES asistentes(id),
            FOREIGN KEY (caso_id) REFERENCES casos(id)
        );
        """)
        
        connection.commit()
        print("Tabla 'tickets' creada exitosamente.")

    except sqlite3.Error as e:
        print(f"Error al crear la tabla 'tickets': {e}")
    finally:
        if connection:
            connection.close()

def insert_sample_tickets_data(db_path="crm_law_firm.db"):
    """
    Inserta 30 filas de datos de ejemplo en la tabla 'tickets'.
    """
    estados = ['abierto', 'cerrado']
    notas = [
        "Revisar documentos pendientes.",
        "Preparar evidencia para el caso.",
        "Enviar notificación al cliente.",
        "Revisar plazos de entrega.",
        "Coordinar reunión con abogado.",
        "Verificar avances del caso.",
        "Registrar datos adicionales.",
        "Resolver discrepancias en documentos.",
        "Actualizar estado del caso.",
        "Revisar informes semanales."
    ]

    # Generar datos aleatorios para 30 tickets
    tickets_data = []
    today = datetime.today()

    for _ in range(30):
        asistente_id = random.randint(1, 12)  # ID del asistente entre 1 y 12
        caso_id = random.randint(1, 20)       # ID del caso entre 1 y 20
        estado = random.choice(estados)
        nota = random.choice(notas)
        fecha_creacion = today.strftime('%Y-%m-%d %H:%M:%S')
        fecha_cierre = (
            (today + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d %H:%M:%S') 
            if estado == 'cerrado' else None
        )
        tickets_data.append((asistente_id, caso_id, estado, nota, fecha_creacion, fecha_cierre))

    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Insertar datos en la tabla 'tickets'
        cursor.executemany("""
        INSERT INTO tickets (asistente_id, caso_id, estado, nota, fecha_creacion, fecha_cierre)
        VALUES (?, ?, ?, ?, ?, ?);
        """, tickets_data)
        
        connection.commit()
        print("Datos insertados exitosamente en la tabla 'tickets'.")

    except sqlite3.Error as e:
        print(f"Error al insertar datos en 'tickets': {e}")
    finally:
        if connection:
            connection.close()


def get_total_records(table_name):
    conn = conectar()
    cursor = conn.cursor()
    
    # Consulta dinámica con el nombre de la tabla
    query = f"SELECT COUNT(*) FROM {table_name}"
    cursor.execute(query)
    total_records = cursor.fetchone()[0]
    
    conn.close()
    return total_records

def get_records(table_name, order_by, order_direction='asc', limit=10, offset=0):
    """
    Obtiene los registros de una tabla específica y los ordena por el campo `order_by`.
    """
    conn = conectar()
    cursor = conn.cursor()

    # Validar entrada para evitar inyección SQL
    if order_direction not in ['asc', 'desc']:
        order_direction = 'asc'

    # Usar parámetros dinámicos y construir la consulta
    query = f"SELECT * FROM {table_name} ORDER BY {order_by} {order_direction} LIMIT ? OFFSET ?"
    cursor.execute(query, (limit, offset))
    records = cursor.fetchall()
    
    conn.close()
    return records
