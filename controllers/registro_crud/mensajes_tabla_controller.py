#################################################################################################
#################################################################################################

# controller_mensajes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import get_db

mensajes_bp = Blueprint("mensajes_bp", __name__)

# ============================================================
# LISTAR MENSAJES DE UNA CONVERSACIÓN
# ============================================================

@mensajes_bp.route("/mensajes")
def listar_mensajes():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM MENSAJE ORDER BY Fecha_hora DESC")
    
    mensajes = cursor.fetchall()
    ##print("📌 DATOS:", mensajes) La información sí se está trayendo, todo bien por aquí.
    
    cursor.close()
    conn.close()

    return render_template("registros_crud/mensajes_tabla.html", mensajes=mensajes)

# ============================================================
# LISTAR MENSAJES DE UNA CONVERSACIÓN
# ============================================================




################################################################################################
################################################################################################