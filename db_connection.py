import sqlite3

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


# conectar()
# create_abogados_table()
# insert_sample_abogados_data()
# fetch_and_display_abogados()
