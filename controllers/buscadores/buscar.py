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
    resultados = []

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        sql = """
            SELECT *
            FROM solicitante
            WHERE cedula::TEXT        ILIKE %s
               OR nombre              ILIKE %s
               OR tipo_solicitante    ILIKE %s
        """

        like = f"%{q}%"
        cursor.execute(sql, (like, like, like))
        resultados = cursor.fetchall()

    except Error as e:
        print(f"Error al buscar solicitantes: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/solicitantes_tabla.html",
        solicitantes=resultados
    )