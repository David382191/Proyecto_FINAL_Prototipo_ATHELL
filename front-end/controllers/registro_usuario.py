## Alfonso Espinoza
from flask import Blueprint, render_template, session, redirect
from database.db import get_connection

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/usuarios")
def usuarios_panel():
    if "admin_id" not in session:
        return redirect("/")
    
    # Consultar los usuarios de la BD si quieres
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM administrador_secretaria")  # Ejemplo
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template("registro-usuarios.html", usuarios=usuarios)
