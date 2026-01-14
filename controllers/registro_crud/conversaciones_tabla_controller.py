################################################################################################
################################################################################################

# controller_conversaciones.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector
from database.db import get_db

conversaciones_bp = Blueprint("conversaciones_bp", __name__)

# ============================================================
# LISTAR TODAS LAS CONVERSACIONES
# ============================================================
@conversaciones_bp.route("/conversaciones")
def listar_conversaciones():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CONVERSACION ORDER BY Fecha_inicio DESC")
    conversaciones = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("registros_crud/conversaciones_tabla.html", conversaciones=conversaciones)
# ============================================================
# BUSCAR (por ID o Cédula)
# ============================================================
@conversaciones_bp.route("/buscar-conversaciones")
def buscar_conversaciones():
    q = request.args.get("q", "").strip()

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT * FROM CONVERSACION
        WHERE ID_CONVERSACION LIKE %s OR CEDULA_SOLICITANTE LIKE %s
    """

    print("📌 DATOS:", sql)

    like = f"%{q}%"
    cursor.execute(sql, (like, like))

    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("registros_crud/conversaciones_tabla.html", conversaciones=resultados)
# ============================================================
# MOSTRAR MENSAJES DE UNA CONVERSACIÓN
# (Esto asume que tienes otra tabla MENSAJE)
# ============================================================

################################################################################################
################################################################################################