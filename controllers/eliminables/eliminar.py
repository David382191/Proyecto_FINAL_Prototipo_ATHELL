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