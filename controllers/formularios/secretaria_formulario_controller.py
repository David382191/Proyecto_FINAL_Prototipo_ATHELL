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
@secretaria_form_bp.route("/crear-secretaria", methods=["POST"])
def crear_secretaria():

    # 1️⃣ Obtener datos del formulario
    cedula = request.form.get("CEDULA")
    nombre = request.form.get("Nombre")
    apellido = request.form.get("Apellido")
    usuario = request.form.get("Usuario")
    contrasena = request.form.get("Contrasena")
    telefono = request.form.get("Telefono")

    # 2️⃣ Validaciones básicas
    if not cedula or not nombre or not apellido or not usuario or not contrasena:
        flash("Todos los campos obligatorios deben llenarse", "danger")
        return redirect(url_for("home_bp.nueva_secretaria"))

    # 3️⃣ Hashear contraseña
    password_hash = generate_password_hash(contrasena)

    # 4️⃣ Guardar en la base de datos
    # EJEMPLO CON SQLALCHEMY
    from models.secretaria import Secretaria
    from app import db

    nueva = Secretaria(
        cedula=cedula,
        nombre=nombre,
        apellido=apellido,
        usuario=usuario,
        contrasena=password_hash,
        telefono=telefono
    )

    db.session.add(nueva)
    db.session.commit()

    # 5️⃣ Mensaje y redirección
    flash("Secretaria creada correctamente", "success")
    return redirect(url_for("home_bp.panel_administradores"))
###################################################################################################
