################################################################################################
################################################################################################
# controller_conversaciones.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector
from database.db import get_db
from psycopg2.extras import RealDictCursor
from psycopg2 import Error
################################################################################################
conversaciones_bp = Blueprint("conversaciones_bp", __name__)
# ============================================================
# 1- LISTAR TODAS LAS CONVERSACIONES
# ============================================================
@conversaciones_bp.route("/conversaciones")
def listar_conversaciones():
    conn = None
    cursor = None
    conversaciones = []

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT *
            FROM conversacion
            ORDER BY fecha_inicio DESC
        """)
        conversaciones = cursor.fetchall()

    except Error as e:
        print(f"Error al listar conversaciones: {e}")
        conversaciones = []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/conversaciones_tabla.html",
        conversaciones=conversaciones
    )
# ============================================================
# 2- BUSCAR (por ID o Cédula)
# ============================================================

# ============================================================
# 3- MOSTRAR MENSAJES DE UNA CONVERSACIÓN
# (Esto asume que tienes otra tabla MENSAJE)
# ============================================================
@conversaciones_bp.route("/mensajes/<int:id_conversacion>")
def ver_mensajes(id_conversacion):
    conn = None
    cursor = None
    mensajes = []

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Traer todos los mensajes de esa conversación
        cursor.execute("""
            SELECT *
            FROM mensaje
            WHERE id_conversacion = %s
            ORDER BY fecha_hora ASC
        """, (id_conversacion,))

        mensajes = cursor.fetchall()

    except Error as e:
        print(f"Error al obtener mensajes: {e}")
        mensajes = []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/mensajes_tabla.html",
        mensajes=mensajes
    )
################################################################################################
################################################################################################