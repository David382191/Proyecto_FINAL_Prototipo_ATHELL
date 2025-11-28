################################################################################################
################################################################################################

# controller_conversaciones.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector

conversaciones_bp = Blueprint("conversaciones_bp", __name__)

# ---------------------------
# CONEXIÓN A LA BD
# ---------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port="3307",
        user="root",
        password="12345",
        database="chatbot_secretaria",
    )


# ============================================================
# LISTAR TODAS LAS CONVERSACIONES
# ============================================================
@conversaciones_bp.route("/conversaciones")
def listar_conversaciones():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CONVERSACION ORDER BY Fecha_inicio DESC")
    conversaciones = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("panel_conversaciones.html", conversaciones=conversaciones)


# ============================================================
# BUSCAR (por ID o Cédula)
# ============================================================
@conversaciones_bp.route("/buscar-conversaciones")
def buscar_conversaciones():
    q = request.args.get("q", "").strip()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM CONVERSACION
        WHERE ID_CONVERSACION LIKE %s OR CEDULA_SOLICITANTE LIKE %s
    """
    like = f"%{q}%"
    cursor.execute(query, (like, like))

    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("panel_conversaciones.html", conversaciones=resultados)


# ============================================================
# MOSTRAR MENSAJES DE UNA CONVERSACIÓN
# (Esto asume que tienes otra tabla MENSAJE)
# ============================================================
@conversaciones_bp.route("/conversacion/<int:id>")
def ver_conversacion(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener datos principales
    cursor.execute("SELECT * FROM CONVERSACION WHERE ID_CONVERSACION = %s", (id,))
    conv = cursor.fetchone()

    # Obtener mensajes asociados
    cursor.execute("""
        SELECT * FROM MENSAJE WHERE ID_CONVERSACION = %s ORDER BY Fecha ASC
    """, (id,))
    mensajes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("ver_conversacion.html", conversacion=conv, mensajes=mensajes)


# ============================================================
# IMPRIMIR CONVERSACIÓN (versión simple)
# ============================================================
@conversaciones_bp.route("/imprimir-conversacion/<int:id>")
def imprimir_conversacion(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM CONVERSACION WHERE ID_CONVERSACION = %s", (id,))
    conv = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM MENSAJE WHERE ID_CONVERSACION = %s ORDER BY Fecha ASC
    """, (id,))
    mensajes = cursor.fetchall()

    cursor.close()
    conn.close()

    # Renderiza un HTML que el navegador puede imprimir
    return render_template("imprimir_conversacion.html", conversacion=conv, mensajes=mensajes)


# ============================================================
# ELIMINAR CONVERSACIÓN
# ============================================================
@conversaciones_bp.route("/eliminar-conversacion/<int:id>", methods=["POST", "GET"])
def eliminar_conversacion(id):

    conn = get_connection()
    cursor = conn.cursor()

    # Primero borrar los mensajes asociados (si existen)
    cursor.execute("DELETE FROM MENSAJE WHERE ID_CONVERSACION = %s", (id,))

    # Luego borrar la conversación
    cursor.execute("DELETE FROM CONVERSACION WHERE ID_CONVERSACION = %s", (id,))
    
    conn.commit()
    cursor.close()
    conn.close()

    flash("Conversación eliminada correctamente", "success")
    return redirect(url_for("conversaciones_bp.listar_conversaciones"))


################################################################################################
################################################################################################