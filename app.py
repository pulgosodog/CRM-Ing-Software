from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash, jsonify, session

from datetime import datetime

from db_connection import get_total_records, get_records, insertar_cliente, get_cases_join, get_total_records_by_client, get_where, get_id_cliente_from_tickets, conectar, login_required, role_required


views = Blueprint('views', __name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar flash mensajes

@app.route('/')
@login_required
def home():
    user_name = None
    # user_tickets = []
    # user_cases = []
    if session['rol'] == 'abogado' and session.get('id_abogado'):
        user_data = get_where('abogados', 'id', session['id_abogado'])
        # user_tickets = get_user_related_data('abogado', session['id_abogado'], 'tickets', 'id_abogado', 'fecha')
        # user_cases = get_user_related_data('abogado', session['id_abogado'], 'casos', 'id_abogado', 'fecha')
    elif session['rol'] == 'asistente' and session.get('id_asistente'):
        user_data = get_where('asistentes', 'id', session['id_asistente'])
        # user_tickets = get_where('asistente', session['id_asistente'], 'tickets', 'id_asistente', 'fecha')
        # user_cases = get_user_related_data('asistente', session['id_asistente'], 'casos', 'id_asistente', 'fecha')
    nombre = user_data[0]['nombre_completo']
    message = "Report"
    return render_template('report.html', message=message, nombre = nombre)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, rol, id_abogado, id_asistente FROM usuarios WHERE username = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()
        
        if user:
            session['username'] = user[0]
            session['rol'] = user[1]
            session['id_abogado'] = user[2]
            session['id_asistente'] = user[3]
            return redirect('/')
        else:
            return render_template('login.html', error_message= True)
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/contacts', defaults={'page': 1, 'order_by': 'nombre_completo', 'order_direction': 'asc'})
@app.route('/contacts/page/<int:page>/<order_by>/<order_direction>')
@login_required
def contacts(page, order_by, order_direction):
    per_page = 10  # Número de registros por página
    offset = (page - 1) * per_page  # Calcular el desplazamiento

    # Obtener los clientes con paginación y orden dinámico
    clientes = get_records('clientes', order_by=order_by, order_direction=order_direction, limit=per_page, offset=offset)

    # Obtener el número total de registros para calcular el número de páginas
    total_records = get_total_records('clientes')
    total_pages = (total_records + per_page - 1) // per_page  # Redondeo hacia arriba

    # Pasar los datos y las variables necesarias al template
    return render_template(
        "contacts.html",
        clientes=clientes,
        current_page=page,
        total_pages=total_pages,
        message="Clientes",
        order_by=order_by,
        order_direction=order_direction
    )

@app.route('/add-client', methods=['POST'])
@login_required
def add_client():
    try:

        # Asegurarse de recibir JSON
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No se enviaron datos'}), 400

        # Imprimir los datos recibidos para depuración
        print("Datos recibidos en el backend:", data)

        # Extraer datos del JSON recibido
        nombre_completo = data.get('nombre_completo')
        telefono = data.get('telefono')
        email = data.get('email')
        preferencias = data.get('preferencias')
        fecha_nacimiento = data.get('fecha_nacimiento')
        notas = data.get('notas')

        # Validar datos esenciales
        if not nombre_completo or not email:
            return jsonify({'message': 'El nombre completo y el email son obligatorios'}), 400

        # Llamar a la función para insertar en la base de datos
        if insertar_cliente(nombre_completo, telefono, email, preferencias, fecha_nacimiento, notas):
            return jsonify({'message': 'Cliente agregado exitosamente'}), 200
        else:
            return jsonify({'message': 'Error al agregar cliente. Puede que el email ya esté registrado.'}), 400

    except Exception as e:
        print(f"Error en la ruta /add-client: {e}")
        return jsonify({'message': 'Error en el servidor'}), 500


@app.route('/tickets', defaults={'page': 1, 'order_by': 'id', 'order_direction': 'asc'})
@app.route('/tickets/page/<int:page>/<order_by>/<order_direction>')
@login_required
def tickets(page, order_by, order_direction):
    per_page = 10  # Número de registros por página
    offset = (page - 1) * per_page  # Calcular el desplazamiento

    # Obtener los tickets con paginación y orden dinámico
    tickets = get_records('tickets', order_by=order_by, order_direction=order_direction, limit=per_page, offset=offset)

    # Obtener el número total de registros para calcular el número de páginas
    total_records = get_total_records('tickets')
    total_pages = (total_records + per_page - 1) // per_page  # Redondeo hacia arriba

    def calcular_prioridad(fecha_tope):

        # Verificar si fecha_tope es una cadena de texto
        if isinstance(fecha_tope, str):
            try:
                # Parsear la fecha con el formato adecuado
                fecha_tope_obj = datetime.strptime(fecha_tope, '%Y-%m-%d %H:%M:%S')

                # Extraer solo la fecha (sin la hora)
                fecha_tope_obj = fecha_tope_obj.date()

                # Calcular la diferencia de días entre la fecha actual y la fecha tope
                hoy = datetime.today().date()
                diferencia_dias = (fecha_tope_obj - hoy).days

                # Asignar la prioridad según los días restantes
                if diferencia_dias <= 3:
                    prioridad = 'Alta'
                elif diferencia_dias <= 7:
                    prioridad = 'Media'
                else:
                    prioridad = 'Baja'

                return prioridad

            except ValueError:
                print("Formato de fecha incorrecto. Asegúrate de que esté en formato 'YYYY-MM-DD HH:MM:SS'")
        else:
            print("Fecha tope no es una cadena de texto válida.")


    # Pasar los datos y las variables necesarias al template
    return render_template(
        "tickets.html",
        tickets=tickets,
        current_page=page,
        total_pages=total_pages,
        message="Tickets",
        order_by=order_by,
        order_direction=order_direction,
        fecha_tope = calcular_prioridad(tickets[7][7])
    )

@app.route('/client/<int:client_id>', defaults={'client_id': 1})
@app.route('/client/<int:client_id>')
@login_required
def client_serve_by_id(client_id):
    info = get_where("clientes","id", get_id_cliente_from_tickets(client_id),"nombre_completo")
    return jsonify(info)

@app.route('/cases', defaults={'page': 1, 'order_by': 'nombre_caso', 'order_direction': 'asc'})
@app.route('/cases/page/<int:page>/<order_by>/<order_direction>')
@login_required
def cases(page, order_by, order_direction):
    message = "Casos"
    per_page = 9  # Número de registros por página
    offset = (page - 1) * per_page  # Calcular el desplazamiento para la paginación

    # Obtener los casos con paginación y orden dinámico
    casos = get_cases_join(order_by=order_by, order_direction=order_direction, limit=per_page, offset=offset)
    # Obtener el número total de registros para calcular el número de páginas
    total_records = get_total_records('casos')
    total_pages = (total_records + per_page - 1) // per_page  # Redondeo hacia arriba

    # Pasar los datos y las variables necesarias al template
    return render_template(
        "cases.html",
        casos=casos,
        current_page=page,
        total_pages=total_pages,
        message=message,
        order_by=order_by,
        order_direction=order_direction
    )

@app.route('/cases/client/<int:client_id>', defaults={'page': 1, 'order_by': 'nombre_caso', 'order_direction': 'asc'})
@app.route('/cases/client/<int:client_id>/page/<int:page>/<order_by>/<order_direction>')
@login_required
def cases_by_client(client_id, page, order_by, order_direction):
    message = f"Casos del Cliente {client_id}"
    per_page = 9  # Número de registros por página
    offset = (page - 1) * per_page  # Calcular el desplazamiento para la paginación

    # Obtener los casos filtrados por el ID del cliente
    casos = get_cases_join(client_id=client_id, order_by=order_by, order_direction=order_direction, limit=per_page, offset=offset)
    
    # Obtener el número total de registros para calcular el número de páginas
    total_records = get_total_records_by_client(client_id)
    total_pages = (total_records + per_page - 1) // per_page  # Redondeo hacia arriba

    # Pasar los datos y las variables necesarias al template
    return render_template(
        "cases.html",
        casos=casos,
        current_page=page,
        total_pages=total_pages,
        message=message,
        order_by=order_by,
        order_direction=order_direction
    )

@app.route('/cases/<int:case_id>', defaults={'case_id': 1})
@app.route('/cases/<int:case_id>')
@login_required
def tickets_cases_serve(case_id):
    notas = get_where("tickets","caso_id", case_id,"fecha_tope")
    return jsonify(notas)

@app.route('/asistente/<int:asistente_id>', defaults={'asistente_id': 1})
@app.route('/asistente/<int:asistente_id>')
@login_required
def get_asistente(asistente_id):
    info = get_where("asistentes","id", asistente_id,"nombre_completo")
    return jsonify(info)

@app.route('/report')
@login_required
def report():
    message = "Report"
    return render_template('report.html', message=message)

@app.route('/calendar')
@login_required
def calendar():
    message = "Calendar"
    return render_template('calendar.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
# BUSCAR EL IP LOCAL PONIENDO EN LA TERMINAL: ipconfig
# LUEGO USAR ESTE LINK: http://<your-local-ip>:5000


