###################################################################################################
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from database.db import get_db
from psycopg2.extras import RealDictCursor
from psycopg2 import Error
###################################################################################################
# Blueprint
eliminar_bp = Blueprint("eliminar_bp", __name__)
###################################################################################################
@eliminar_bp.route("/eliminar-entrada/<int:id_entrada>")
def eliminar_entrada(id_entrada):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM diario_entrada
            WHERE id_entrada = %s
        """, (id_entrada,))

        conn.commit()

    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error al eliminar Entrada: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect("/entradasdiario")
###################################################################################################
@eliminar_bp.route("/eliminar-palabra/<int:id_pc>")
def eliminar_palabra(id_pc):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM palabra_clave
            WHERE id_pc = %s
        """, (id_pc,))

        conn.commit()

    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error al eliminar palabra clave: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect("/palabrasclave_tabla")  # <-- página donde se muestran las palabras
###################################################################################################
@eliminar_bp.route("/eliminar-mensaje/<int:id_mensaje>")
def eliminar_mensaje(id_mensaje):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM mensaje
            WHERE id_mensaje = %s
        """, (id_mensaje,))

        conn.commit()

    except Exception as e:  # Puedes usar Error si lo importaste de psycopg2
        if conn:
            conn.rollback()
        print(f"Error al eliminar mensaje: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect("/mensajes_tabla")  # <-- página donde se muestran los mensajes
#################################################################################################
@eliminar_bp.route("/eliminar-conversacion/<int:id_conversacion>")
def eliminar_conversacion(id_conversacion):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM conversacion
            WHERE id_conversacion = %s
        """, (id_conversacion,))

        conn.commit()

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error al eliminar conversación: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect("/conversaciones_tabla")  # <-- página donde se muestran las conversaciones
#################################################################################################