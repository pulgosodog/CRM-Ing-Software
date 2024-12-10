from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
from functools import wraps
from datetime import datetime, timedelta
from datetime import datetime

app = Flask(__name__)

DATABASE = 'crm_law_firm.db'

def conectar():
    """
    Crea y retorna una conexión a la base de datos 'crm_law_firm.db'.
    Si ya existe una conexión en 'g', la reutiliza.
    """
    if 'db' not in g:  
        try:
            g.db = sqlite3.connect(DATABASE)
            g.db.row_factory = sqlite3.Row  
            print("Conexión exitosa a la base de datos")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            g.db = None
    return g.db

@app.teardown_appcontext
def cerrar_conexion(conexion=None):
    """
    Cierra la conexión activa a la base de datos.
    Si hay una conexión en 'g', también la cierra.
    """
    if 'db' in g:  
        g.db.close()
        g.pop('db', None)
        print("Conexión cerrada exitosamente")
    elif conexion:  
        conexion.close()
        print("Conexión cerrada exitosamente")

def get_total_records(table_name):
    conn = conectar()
    cursor = conn.cursor()
    
    
    query = f"SELECT COUNT(*) FROM {table_name}"
    cursor.execute(query)
    total_records = cursor.fetchone()[0]
    
    return total_records

def get_records(table_name, order_by, order_direction='asc', limit=10, offset=0):
    """
    Obtiene los registros de una tabla específica y los ordena por el campo `order_by`.
    """
    conn = conectar()
    cursor = conn.cursor()

    
    if order_direction not in ['asc', 'desc']:
        order_direction = 'asc'

    
    query = f"SELECT * FROM {table_name} ORDER BY {order_by} {order_direction} LIMIT ? OFFSET ?"
    cursor.execute(query, (limit, offset))
    records = cursor.fetchall()
    
    return records

def insertar_cliente(nombre_completo, telefono, email, preferencias, fecha_nacimiento, notas):
    """
    Inserta un cliente en la base de datos.
    """
    print("Intentando conectar a la base de datos...")  
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")  
        return False

    try:
        print("Conexión exitosa. Intentando insertar cliente...")  
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre_completo, telefono, email, preferencias, fecha_nacimiento, notas)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre_completo, telefono, email, preferencias, fecha_nacimiento, notas))
        conexion.commit()
        print("Cliente agregado exitosamente.")  
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error al agregar cliente: {e}")  
        return False
    finally:
        cerrar_conexion(conexion)   

def get_cases_join(order_by, order_direction='asc', limit=10, offset=0, client_id=None):
    conn = conectar()
    cursor = conn.cursor()

    
    if order_direction not in ['asc', 'desc']:
        order_direction = 'asc'
    print(order_by)
    
    allowed_columns = [
        "id", "nombre_caso", "tipo_caso", "estado",
        "prioridad", "fecha_creacion", "fecha_deadline",
        "cliente_nombre", "abogado_nombre", "asistente_nombre"
    ]
    if order_by not in allowed_columns:
        order_by = "casos.id"

    
    query = f"""
    SELECT 
    casos.id,
    casos.nombre_caso,
    casos.tipo_caso,
    casos.estado,
    casos.prioridad,
    casos.fecha_creacion,
    casos.fecha_deadline,
    clientes.nombre_completo AS cliente_nombre,
    abogados.nombre_completo AS abogado_nombre,
    asistentes.nombre_completo AS asistente_nombre
    FROM casos
    INNER JOIN clientes ON casos.id_cliente = clientes.id
    LEFT JOIN abogados ON casos.id_abogado = abogados.id
    LEFT JOIN asistentes ON casos.id_asistente = asistentes.id
    """
    
    if client_id:
        query += " WHERE casos.id_cliente = ?"

    
    query += f" ORDER BY {order_by} {order_direction} LIMIT ? OFFSET ?"
    
    if client_id:
        cursor.execute(query, (client_id, limit, offset))
    else:
        cursor.execute(query, (limit, offset))

    records = cursor.fetchall()
    return records

def get_total_records_by_client(client_id):
    conn = conectar()
    cursor = conn.cursor()
    
    
    query = "SELECT COUNT(*) FROM casos WHERE id_cliente = ?"
    cursor.execute(query, (client_id,))
    total_records = cursor.fetchone()[0]

    return total_records

def get_where(table, column, parameter, order_by=None):
    conn = conectar()
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor()
    
    
    query = f"""
    SELECT * FROM {table} 
    WHERE {column} = ?"""
    if order_by:
        query += f" ORDER BY {order_by} DESC"
    
    cursor.execute(query, (parameter,))
    records = cursor.fetchall()
    
    results = [dict(row) for row in records]
    print(results)
    return results

def get_id_cliente_from_tickets(id_ticket):
    conn = conectar()
    cursor = conn.cursor()
    
    query = """
    SELECT clientes.id
    FROM tickets
    JOIN casos ON tickets.caso_id = casos.id
    JOIN clientes ON casos.id_cliente = clientes.id
    WHERE tickets.id = ?;
    """
    cursor.execute(query, (id_ticket,))
    id_cliente = cursor.fetchone()
    
    print("get_id_cliente_from_tickets")
    print(id_cliente)
    return id_cliente[0] if id_cliente else None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('rol') != role:
                return "No tienes acceso a esta página", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
