###################################################################################################
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from database.db import get_db

###################################################################################################
# Blueprint
editar = Blueprint("editar", __name__)
###################################################################################################
@editar.route("/editar/<cedula>", methods=["GET", "POST"])
def editarsecretaria(cedula):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form["Nombre"]
        apellido = request.form["Apellido"]
        telefono = request.form["Telefono"]

        cursor.execute("""
            UPDATE admin_secretaria
            SET Nombre=%s,
                Apellido=%s,
                Telefono=%s
            WHERE CEDULA=%s
        """, (nombre, apellido, telefono, cedula))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("home_bp.panel_administradores"))

    # GET → cargar datos
    cursor.execute(
        "SELECT * FROM admin_secretaria WHERE CEDULA=%s",
        (cedula,)
    )
    secretaria_editar = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "registros_crud/secretaria_tabla.html",
        secretaria_editar=secretaria_editar
    )

###################################################################################################