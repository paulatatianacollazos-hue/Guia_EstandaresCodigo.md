import mysql.connector
from flask import Flask, render_template, request


app = Flask(__name__)
# conoxion a la base de datos
conexion = mysql.connector.connect(
    user="root",
    password="paula123",
    host="localhost",
    database="Casa_En_El_Arbol",
    port="3307",
)
print(conexion)


@app.route("/")
def index():
    precio = 5000
    descripcion = "hola "

    producto = [precio, descripcion]
    data = {"producto": producto, "numero_cursos": len(producto)}

    return render_template("index.html", data=data)


# editar perfil
@app.route("/editar")
def editar():
    return render_template("editar.html")


# modulo de registro
def guardar_en_db(nombre, telefono, contraseña, direccion, correo):
    conn = mysql.connector.connect(**conexion)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nombre,contraseña) VALUES (%s)",
        (
            nombre,
            telefono,
            contraseña,
            direccion,
            correo,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()


@app.route("/registro", methods=["GET", "POST"])
def recoger_input():
    nombre = ""
    telefono = ""
    contraseña = ""
    direccion = ""
    correo = ""

    if request.method == "POST":
        nombre = request.form.get("nombre")
        telefono = request.form.get("telefono")
        contraseña = request.form.get("password")
        direccion = request.form.get("direccion")
        correo = request.form.get("correo")
        guardar_en_db(nombre, telefono, contraseña, direccion, correo)
        # << Llamada correcta

    return render_template("principal.html", nombre=nombre)


# modulo de login
def obtener_validar():
    conn = mysql.connector.connect(**conexion)
    cursor = conn.cursor()
    cursor.execute("SELECT correo, contraseña FROM usuarios")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"correo": fila[0], "contraseña": fila[1]} for fila in resultados]


@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje = ""

    if request.method == "POST":
        correo = request.form.get("correologin")
        contraseña = request.form.get("passwordlogin")

        usuarios = obtener_validar()
        usuario_encontrado = False  # <- bandera para controlar validación

        for user in usuarios:
            if user["correo"] == correo and user["contraseña"] == contraseña:
                mensaje = f"Bienvenido, {correo}"
                usuario_encontrado = True
                break

        if not usuario_encontrado:
            mensaje = "Correo o contraseña incorrectos"

    return render_template("principal.html", mensaje=mensaje)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
