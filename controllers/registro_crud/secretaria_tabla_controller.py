############################################################################################
############################################################################################

from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash
import os

secretaria_bp = Blueprint('secretaria', __name__, template_folder='../templates')

# =====================================================
# CONEXIÓN A MYSQL (ajusta según tu configuración)
# =====================================================
def get_conn():
    return mysql.connector.connect(
        host="localhost",
        port="3307",
        user="root",
        password="12345",
        database="chatbot_secretaria"
    )

# ==========================
# LISTAR SECRETARIAS
# ==========================
@secretaria_bp.route('/lista-secretarias')
def listar_secretarias():
    secretarias = []
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT CEDULA, Nombre, Apellido, Usuario, Telefono FROM ADMIN_SECRETARIA")
        secretarias = cursor.fetchall()
    except Error as e:
        # Puedes mostrar un mensaje o loggear
        flash(f"Error al obtener secretarias: {e}", "danger")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.is_connected(): conn.close()

    return render_template("lista_secretarias.html", secretarias=secretarias)

# ==========================
# CREAR SECRETARIA (GET -> formulario, POST -> guardar)
# ==========================
@secretaria_bp.route('/crear-secretaria', methods=['GET', 'POST'])
def crear_secretaria():
    if request.method == 'GET':
        return render_template("crear_secretaria.html")

    # POST -> procesar formulario
    cedula = request.form.get('CEDULA', '').strip()
    nombre = request.form.get('Nombre', '').strip()
    apellido = request.form.get('Apellido', '').strip()
    usuario = request.form.get('Usuario', '').strip()
    contrasena = request.form.get('Contrasena', '')  # recibimos la contraseña en claro
    telefono = request.form.get('Telefono', '').strip()

    # validaciones básicas
    if not (cedula and nombre and apellido and usuario and contrasena):
        flash("Por favor completa todos los campos obligatorios.", "warning")
        return redirect(url_for('secretaria.crear_secretaria'))

    # hash de la contraseña
    hashed = generate_password_hash(contrasena)  # usa PBKDF2 por defecto

    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = """
            INSERT INTO ADMIN_SECRETARIA
            (CEDULA, Nombre, Apellido, Usuario, Contrasena_hash, Telefono)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (cedula, nombre, apellido, usuario, hashed, telefono or None))
        conn.commit()
        flash("Secretaria creada correctamente.", "success")
        return redirect(url_for('secretaria.listar_secretarias'))

    except mysql.connector.IntegrityError as ie:
        # clave primaria duplicada o usuario duplicado (según constraints)
        flash(f"Error de integridad: {ie}", "danger")
        return redirect(url_for('secretaria.crear_secretaria'))

    except Error as e:
        flash(f"Error al crear secretaria: {e}", "danger")
        return redirect(url_for('secretaria.crear_secretaria'))

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.is_connected(): conn.close()

# ==========================
# EDITAR y ELIMINAR (esqueleto)
# ==========================
@secretaria_bp.route('/editar-secretaria/<cedula>', methods=['GET', 'POST'])
def editar_secretaria(cedula):
    # Implementa según necesidad: GET -> mostrar formulario con datos; POST -> actualizar
    flash("Funcionalidad de edición no implementada aún.", "info")
    return redirect(url_for('secretaria.listar_secretarias'))

@secretaria_bp.route('/eliminar-secretaria/<cedula>', methods=['GET'])
def eliminar_secretaria(cedula):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ADMIN_SECRETARIA WHERE CEDULA = %s", (cedula,))
        conn.commit()
        flash("Secretaria eliminada.", "success")
    except Error as e:
        flash(f"Error al eliminar: {e}", "danger")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.is_connected(): conn.close()
    return redirect(url_for('secretaria.listar_secretarias'))

############################################################################################
############################################################################################