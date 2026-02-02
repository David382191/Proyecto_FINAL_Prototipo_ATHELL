###################################################################################################
###################################################################################################
from flask import Blueprint, render_template, request, redirect, url_for, flash, Flask
from werkzeug.security import generate_password_hash
from database.db import get_db
import mysql.connector
from psycopg2.extras import RealDictCursor
from psycopg2 import Error
###################################################################################################
###################################################################################################
# Blueprint
secretaria_form_bp = Blueprint("secretaria_form_bp", __name__)
###################################################################################################
###################################################################################################
# ==========================
# 1. MOSTRAR FORMULARIO
# ==========================
@secretaria_form_bp.route("/nueva-secretaria")
def nueva_secretaria():
    return render_template("secretaria_formulario.html")
# ==========================
# 2. PROCESAR FORMULARIO
# ==========================
@secretaria_form_bp.route("/crear-secretaria", methods=["GET", "POST"])
def crear_secretaria():
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        if request.method == "POST":

            # 🔴 VALIDACIÓN
            cedula = request.form.get("cedula", "").strip()
            nombre = request.form.get("nombre", "").strip()
            apellido = request.form.get("apellido", "").strip()
            usuario = request.form.get("usuario", "").strip()
            contrasena = request.form.get("contrasena_hash", "").strip()
            telefono = request.form.get("telefono", "").strip()

            if not cedula or not nombre or not apellido or not usuario or not telefono:
                flash("Todos los campos son obligatorios", "danger")
                return redirect(request.url)

            # 🟢 INSERT
            cursor.execute("""
                INSERT INTO admin_secretaria
                (cedula, nombre, apellido, usuario, contrasena_hash, telefono)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (cedula, nombre, apellido, usuario, contrasena, telefono))

            conn.commit()
            return redirect(url_for("home_bp.panel_administradores"))

    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error al crear secretaria: {e}")
        flash("Error al registrar la secretaria", "danger")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template("registro_crud/secretaria_tabla_controller.html")
###################################################################################################
###################################################################################################
@secretaria_form_bp.route('/agregar-admin', methods=['POST'])
def agregar_admin():
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()  # aquí NO necesitamos diccionario

        cedula = request.form['cedula']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']  # ⚠️ luego hashear
        telefono = request.form['telefono']

        # 1️⃣ Validar CÉDULA
        cursor.execute(
            "SELECT COUNT(*) FROM admin_secretaria WHERE cedula = %s",
            (cedula,)
        )
        count_cedula = cursor.fetchone()[0]
        if count_cedula > 0:
            flash("¡Error! Ya existe un admin con esa cédula.", "danger")
            return redirect("/ir-crear-secretaria")

        # 2️⃣ Validar USUARIO
        cursor.execute(
            "SELECT COUNT(*) FROM admin_secretaria WHERE usuario = %s",
            (usuario,)
        )
        count_usuario = cursor.fetchone()[0]
        if count_usuario > 0:
            flash("¡Error! El nombre de usuario ya está en uso.", "danger")
            return redirect("/ir-crear-secretaria")

        # 3️⃣ Insertar registro
        cursor.execute("""
            INSERT INTO admin_secretaria
            (cedula, nombre, apellido, usuario, contrasena_hash, telefono)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (cedula, nombre, apellido, usuario, contrasena, telefono))

        conn.commit()
        flash("Admin agregado correctamente", "success")
        return redirect("/secretaria_tabla")

    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error al agregar admin: {e}")
        flash("Ocurrió un error al agregar el admin", "danger")
        return redirect("/ir-crear-secretaria")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
###################################################################################################
###################################################################################################