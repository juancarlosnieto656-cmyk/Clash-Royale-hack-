from flask import Flask, request, session, redirect, render_template_string
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'una_clave_muy_secreta_y_larga_para_la_sesion'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

intentos_fallidos = {}
bloqueados_permanentemente = []

# Función que verifica seguridad (se usará solo en el panel)
def seguridad_del_panel():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', '').lower()
    
    # 1. Anti-VPN / Anti-Bot
    if not ua or len(ua) < 10 or 'bot' in ua or 'python' in ua or 'curl' in ua:
        return "Acceso denegado: Conexión no segura."
    
    # 2. Bloqueo Hard
    if ip in bloqueados_permanentemente:
        return "DISPOSITIVO BLOQUEADO."
    return None

@app.route('/')
def index():
    # Esta página queda totalmente pública
    return render_template_string(open('index.html').read())

@app.route('/panel', methods=['GET', 'POST'])
def panel():
    # Aplicar seguridad solo aquí
    error_seguridad = seguridad_del_panel()
    if error_seguridad: return error_seguridad
    
    ip = request.remote_addr
    
    # Si ya está logueado, mostrar datos
    if session.get('logged_in'):
        with open('datos.txt', 'r') as f:
            return f"<h1>Panel</h1><pre>{f.read()}</pre><br><a href='/logout'>Cerrar</a>"

    # Gestión de intentos fallidos
    if intentos_fallidos.get(ip, 0) >= 4:
        if request.method == 'POST':
            if request.form.get('pregunta') == 'Mailo y Dante':
                intentos_fallidos[ip] = 0
                session.permanent = True
                session['logged_in'] = True
                return redirect('/panel')
            else:
                bloqueados_permanentemente.append(ip)
                return "RESPUESTA INCORRECTA. Bloqueado."
        return '''<h3>Pregunta de seguridad:</h3><form method="post">¿Cómo se llaman tus perros?: <input type="text" name="pregunta"><br><input type="submit" value="Entrar"></form>'''

    # Login normal
    if request.method == 'POST':
        if request.form.get('usuario') == 'juanc._25' and request.form.get('pass') == 'elprofre':
            session.permanent = True
            session['logged_in'] = True
            intentos_fallidos[ip] = 0
            return redirect('/panel')
        else:
            intentos_fallidos[ip] = intentos_fallidos.get(ip, 0) + 1
            return "Clave incorrecta. <a href='/panel'>Volver</a>"
            
    return '''<h3>Login Panel</h3><form method="post">Usuario: <input type="text" name="usuario"><br>Clave: <input type="password" name="pass"><br><input type="submit" value="Entrar"></form>'''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/panel')

if __name__ == '__main__':
    app.run()

