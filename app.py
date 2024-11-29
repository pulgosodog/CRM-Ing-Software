from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash, jsonify

from db_connection import get_total_records, get_records, insertar_cliente

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

@app.route('/tickets')
def tickets():
    message = "Tickets"
    return render_template('tickets.html', message=message)

@app.route('/cases', defaults={'page': 1, 'order_by': 'nombre_caso', 'order_direction': 'asc'})
@app.route('/cases/page/<int:page>/<order_by>/<order_direction>')
def cases(page, order_by, order_direction):
    message = "Casos"
    per_page = 9  # Número de registros por página
    offset = (page - 1) * per_page  # Calcular el desplazamiento para la paginación

    # Obtener los casos con paginación y orden dinámico
    casos = get_records('casos', order_by=order_by, order_direction=order_direction, limit=per_page, offset=offset)

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


