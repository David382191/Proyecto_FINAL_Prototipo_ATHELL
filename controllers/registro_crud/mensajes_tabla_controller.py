#################################################################################################
#################################################################################################
# controller_mensajes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import get_db
from psycopg2.extras import RealDictCursor
from psycopg2 import Error
#################################################################################################
mensajes_bp = Blueprint("mensajes_bp", __name__)
# ============================================================
# LISTAR MENSAJES DE UNA CONVERSACIÓN
# ============================================================
@mensajes_bp.route("/listar_mensajes")
def listar_mensajes():
    conn = None
    cursor = None
    m = []

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT *
            FROM mensaje
            ORDER BY fecha_hora DESC
        """)

        m = cursor.fetchall()

    except Error as e:
        print(f"Error al listar mensajes: {e}")
        m = []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/mensajes_tabla.html",
        m=m
    )
# ============================================================
# LISTAR MENSAJES DE UNA CONVERSACIÓN
# ============================================================
@mensajes_bp.route("/buscar-mensajes")
def buscar_mensajes():
    q = request.args.get("q", "").strip()
    like = f"%{q}%"

    conn = None
    cursor = None
    m = []

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT *
            FROM mensaje
            WHERE CAST(id_mensaje AS TEXT) ILIKE %s
               OR CAST(id_conversacion AS TEXT) ILIKE %s
               OR remitente ILIKE %s
               OR CAST(fecha_hora AS TEXT) ILIKE %s
        """, (like, like, like, like))

        m = cursor.fetchall()

    except Error as e:
        print(f"Error al buscar mensajes: {e}")
        m = []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/mensajes_tabla.html",
        m=m
    )
################################################################################################
################################################################################################