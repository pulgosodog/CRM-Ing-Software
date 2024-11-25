from flask import Flask, render_template, Blueprint
from db_connection import get_total_records, get_records

views = Blueprint('views', __name__)

app = Flask(__name__)

@app.route('/')
def home():
    message = "Elige una herramienta"
    return render_template('index.html', message=message)

@app.route('/contacts', defaults={'page': 1, 'order_by': 'nombre_completo'})
@app.route('/contacts/page/<int:page>/<order_by>')
def contacts(page, order_by):
    per_page = 10  # Número de registros por página
    offset = (page - 1) * per_page  # Calcular el desplazamiento

    # Obtener los clientes con paginación y orden por el campo que se pase
    clientes = get_records('clientes', order_by=order_by, limit=per_page, offset=offset)

    # Obtener el número total de registros para calcular el número de páginas
    total_records = get_total_records('clientes')
    total_pages = (total_records + per_page - 1) // per_page  # Redondeo hacia arriba

    # Pasar los datos y las variables necesarias al template
    return render_template(
        "contacts.html",
        clientes=clientes,
        current_page=page,
        total_pages=total_pages,
        message="Clientes"
    )


@app.route('/tickets')
def tickets():
    message = "Tickets"
    return render_template('tickets.html', message=message)

@app.route('/cases')
def cases():
    message = "Casos"
    return render_template('cases.html', message=message)

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


