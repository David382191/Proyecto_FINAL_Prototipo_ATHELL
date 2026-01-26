###################################################################################################
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from database.db import get_db

# Blueprint
secretaria_form_bp = Blueprint("secretaria_form_bp", __name__)

# ==========================
# MOSTRAR FORMULARIO
# ==========================
@secretaria_form_bp.route("/nueva-secretaria")
def nueva_secretaria():
    return render_template("secretaria_formulario.html")


# ==========================
# PROCESAR FORMULARIO
# ==========================
@secretaria_form_bp.route("/crear-secretaria", methods=["GET", "POST"])
def crear_secretaria():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        # 🔴 VALIDACIÓN (AQUÍ VA)
        cedula = request.form.get("CEDULA", "").strip()
        nombre = request.form.get("Nombre", "").strip()
        apellido = request.form.get("Apellido", "").strip()
        usuario = request.form.get("Usuario", "").strip()
        contrasena = request.form.get("Contrasena_hash", "").strip()
        telefono = request.form.get("Telefono", "").strip()

        if not cedula or not nombre or not apellido or not usuario or not telefono:
            flash("Todos los campos son obligatorios", "danger")
            cursor.close()
            conn.close()
            return redirect(request.url)

        # 🟢 INSERT SOLO SI TODO ESTÁ BIEN
        cursor.execute("""
            INSERT INTO admin_secretaria
            (CEDULA, Nombre, Apellido, Usuario, Contrasena_hash, Telefono)
            VALUES (%s, %s, %s, %s, %s)
        """, (cedula, nombre, apellido, usuario, contrasena, telefono))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("home_bp.panel_administradores"))

    return render_template("registro_crud/secretaria_tabla_controller.html")

###################################################################################################
