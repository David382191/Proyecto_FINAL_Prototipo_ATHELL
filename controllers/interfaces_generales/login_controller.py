## Por Alfonso Espinoza
###################################################
from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from database.db import get_db
import psycopg2
from psycopg2 import Error
from werkzeug.security import check_password_hash  # si usas hash
###################################################
login_bp = Blueprint("login_bp", __name__)
###################################################
@login_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("interfaces_generales/login.html")

    # Obtener datos del formulario
    username = request.form.get("username")
    password = request.form.get("password")

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        # Buscar usuario en la base de datos
        cursor.execute(
            "SELECT nombre, apellido, usuario, contrasena_hash FROM admin_secretaria WHERE usuario = %s",
            (username,)
        )
        row = cursor.fetchone()

        if row:
            nombre, apellido, db_usuario, db_contrasena = row
            if password == db_contrasena:
                session['usuario_nombre'] = f"{nombre} {apellido}"
                return redirect(url_for("login_bp.home"))


            # ✅ Si usas hash (recomendado):
            # if check_password_hash(db_contrasena, password):
            #     return redirect(url_for("home_bp.home"))

        # Si no encontró usuario o contraseña incorrecta
        flash("Usuario o contraseña incorrectos", "danger")
        return redirect(url_for("login_bp.login"))

    except Error as e:
        print(f"Error en login: {e}")
        flash("Error al intentar conectarse a la base de datos", "danger")
        return redirect(url_for("login_bp.login"))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

            
###################################################

###################################################
# ============================================================
# 1. LISTAR SOLICITANTES
# ============================================================
@login_bp.route("/panel-solicitantes")
def panel_solicitantes():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Administrador_Secretaria")
    solicitantes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "registros_crud/solicitantes_tabla.html",
        solicitantes=solicitantes
    )
############################
@login_bp.route("/home")
def home():
    usuario_nombre = session.get('usuario_nombre', 'Usuario')
    return render_template(
        "interfaces_generales/home.html",
        usuario_nombre=usuario_nombre
    )
############################
##from flask import Blueprint, render_template, session, redirect

