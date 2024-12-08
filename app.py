from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash, jsonify

from datetime import datetime

from db_connection import get_total_records, get_records, insertar_cliente, get_join_case_records, get_cases_join, get_total_records_by_client, get_tickets_case_id


views = Blueprint('views', __name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar flash mensajes

@app.route('/')
def home():
    message = "Elige una herramienta"
    return render_template('index.html', message=message)

@app.route('/contacts', defaults={'page': 1, 'order_by': 'nombre_completo', 'order_direction': 'asc'})
@app.route('/contacts/page/<int:page>/<order_by>/<order_direction>')
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
def add_client():
    try:
        print("Ruta tocada")  # Confirmación de que la ruta es llamada

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

    # Redirige a la página donde se muestran los clientes
    return redirect('/contacts')

@app.route('/tickets', defaults={'page': 1, 'order_by': 'id', 'order_direction': 'asc'})
@app.route('/tickets/page/<int:page>/<order_by>/<order_direction>')
def tickets(page, order_by, order_direction):
    per_page = 10  # Número de registros por página
    offset = (page - 1) * per_page  # Calcular el desplazamiento

    # Obtener los tickets con paginación y orden dinámico
    tickets = get_records('tickets', order_by=order_by, order_direction=order_direction, limit=per_page, offset=offset)

    # Obtener el número total de registros para calcular el número de páginas
    total_records = get_total_records('tickets')
    total_pages = (total_records + per_page - 1) // per_page  # Redondeo hacia arriba

    def calcular_prioridad(fecha_tope):
        # Extraer el valor de la fecha_tope desde la tupla

        # Imprimir el tipo y el valor de fecha_tope para depuración
        print("Tipo de fecha_tope:", type(fecha_tope))
        print("Valor de fecha_tope:", fecha_tope)

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

        
    print("Tipo de fecha_tope:", type(tickets[7]))
    print("Valor de fecha_tope:", tickets[7][7])

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

@app.route('/cases', defaults={'page': 1, 'order_by': 'nombre_caso', 'order_direction': 'asc'})
@app.route('/cases/page/<int:page>/<order_by>/<order_direction>')
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
def tickets_cases_serve(case_id):
    notas = get_tickets_case_id(case_id)
    return jsonify(notas)


@app.route('/report')
def report():
    message = "Report"
    return render_template('report.html', message=message)

@app.route('/calendar')
def calendar():
    message = "Calendar"
    return render_template('calendar.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
# BUSCAR EL IP LOCAL PONIENDO EN LA TERMINAL: ipconfig
# LUEGO USAR ESTE LINK: http://<your-local-ip>:5000


