#################################################################################################
#################################################################################################

# controller_mensajes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector

mensajes_bp = Blueprint("mensajes_bp", __name__)


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
# LISTAR MENSAJES DE UNA CONVERSACIÓN
# ============================================================
@mensajes_bp.route("/mensajes/<int:id_conversacion>")
def listar_mensajes(id_conversacion):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM MENSAJE
        WHERE ID_CONVERSACION = %s
        ORDER BY Fecha_hora ASC
    """, (id_conversacion,))

    mensajes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "mensajes_conversacion.html",
        mensajes=mensajes,
        id_conversacion=id_conversacion
    )


# ============================================================
# BUSCAR MENSAJE DENTRO DE UNA CONVERSACIÓN
# ============================================================
@mensajes_bp.route("/buscar-mensaje/<int:id_conversacion>")
def buscar_mensaje(id_conversacion):

    termino = request.args.get("q", "").strip()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM MENSAJE
        WHERE ID_CONVERSACION = %s
        AND (Contenido LIKE %s OR Remitente LIKE %s)
        ORDER BY Fecha_hora ASC
    """, (id_conversacion, f"%{termino}%", f"%{termino}%"))

    mensajes = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "mensajes_conversacion.html",
        mensajes=mensajes,
        id_conversacion=id_conversacion,
        busqueda=termino
    )


# ============================================================
# ELIMINAR MENSAJE
# ============================================================
@mensajes_bp.route("/eliminar-mensaje/<int:id_mensaje>/<int:id_conversacion>", methods=["POST", "GET"])
def eliminar_mensaje(id_mensaje, id_conversacion):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM MENSAJE WHERE ID_MENSAJE = %s", (id_mensaje,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Mensaje eliminado correctamente", "success")

    return redirect(url_for("mensajes_bp.listar_mensajes", id_conversacion=id_conversacion))


# ============================================================
# IMPRIMIR MENSAJES (vista imprimible)
# ============================================================
@mensajes_bp.route("/imprimir-mensajes/<int:id_conversacion>")
def imprimir_mensajes(id_conversacion):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM MENSAJE
        WHERE ID_CONVERSACION = %s
        ORDER BY Fecha_hora ASC
    """, (id_conversacion,))

    mensajes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "imprimir_mensajes.html",
        mensajes=mensajes,
        id_conversacion=id_conversacion
    )


################################################################################################
################################################################################################