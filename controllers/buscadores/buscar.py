from flask import Blueprint, render_template, request, redirect, url_for, flash
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from database.db import get_db
# ======================================================================================
buscar_bp = Blueprint("buscar_entradas_controller_bp", __name__)
# ======================================================================================
@buscar_bp.route("/buscar-entrada")
def buscar_entrada():
    q = request.args.get("q", "").strip()

    conn = None
    cursor = None
    entradas = []

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        sql = """
            SELECT *
            FROM diario_entrada
            WHERE id_entrada  ILIKE %s
               OR estado      ILIKE %s
               OR titulo      ILIKE %s
        """

        like = f"%{q}%"
        cursor.execute(sql, (like, like, like))
        entradas = cursor.fetchall()

    except Error as e:
        print(f"Error al buscar entradas: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    print(entradas)
    return render_template(
        "registros_crud/entradasdiario_tabla.html",
        entradas=entradas
    )
# ======================================================================================



# ======================================================================================