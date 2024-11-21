from flask import Flask, render_template, Blueprint

views = Blueprint('views', __name__)

app = Flask(__name__)

@app.route('/')
def home():
    message = "Elige una herramienta"
    return render_template('index.html', message=message)

@app.route('/contacts')
def contacts():
    message = "Clientes"
    return render_template('contacts.html', message=message)

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


