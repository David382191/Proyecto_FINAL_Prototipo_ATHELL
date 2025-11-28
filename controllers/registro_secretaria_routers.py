# controllers/secretarias_controller.py

from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
import mysql.connector

# ================================
# BLUEPRINT DEL MÓDULO SECRETARIAS
# ================================
secretarias = Blueprint("secretarias", __name__)


# =============================
# FUNCIÓN DE CONEXIÓN A LA BD
# =============================
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mi_bd"   # <-- Cambia al nombre de tu BD
    )


# =============================
# RUTA PARA LISTAR SECRETARIAS
# =============================
@secretarias.route("/secretarias")
def listar_secretarias():
    db = conectar()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM ADMIN_SECRETARIA")
    datos = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("listar_secretarias.html", secretarias=datos)


# ===========================================
# RUTA CREAR SECRETARIA (GET + POST)
# ===========================================
@secretarias.route("/crear-secretaria", methods=["GET", "POST"])
def crear_secretaria():
    if request.method == "GET":
        return render_template("crear_secretaria.html")

    # === 1. Recibir datos del formulario ===
    cedula = request.form["CEDULA"]
    nombre = request.form["Nombre"]
    apellido = request.form["Apellido"]
    usuario = request.form["Usuario"]
    contrasena_plana = request.form["Contrasena_hash"]
    telefono = request.form["Telefono"]

    # === 2. Convertir contraseña a hash ===
    contrasena_hash = generate_password_hash(contrasena_plana)

    # === 3. Guardar en BD ===
    db = conectar()
    cursor = db.cursor()

    sql = """
        INSERT INTO ADMIN_SECRETARIA
        (CEDULA, Nombre, Apellido, Usuario, Contrasena_hash, Telefono)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    datos = (cedula, nombre, apellido, usuario, contrasena_hash, telefono)

    try:
        cursor.execute(sql, datos)
        db.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
        flash("Error al guardar: probablemente el usuario ya existe.", "danger")
        return redirect("/crear-secretaria")

    cursor.close()
    db.close()

    flash("Secretaria creada exitosamente.", "success")
    return redirect("/secretarias")


# ===========================================
# RUTA PARA ELIMINAR UNA SECRETARIA
# ===========================================
@secretarias.route("/eliminar-secretaria/<cedula>")
def eliminar_secretaria(cedula):
    db = conectar()
    cursor = db.cursor()

    cursor.execute("DELETE FROM ADMIN_SECRETARIA WHERE CEDULA = %s", (cedula,))
    db.commit()

    cursor.close()
    db.close()

    flash("Secretaria eliminada.", "success")
    return redirect("/secretarias")


# ===========================================
# RUTA PARA VER DETALLES
# ===========================================
@secretarias.route("/ver-secretaria/<cedula>")
def ver_secretaria(cedula):
    db = conectar()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM ADMIN_SECRETARIA WHERE CEDULA = %s", 
        (cedula,)
    )
    secretaria = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template("formulario_secretaria.html", secretaria=secretaria)
