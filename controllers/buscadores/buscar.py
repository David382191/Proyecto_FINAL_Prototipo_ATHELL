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
@buscar_bp.route("/buscar-palabra")
def buscar_palabra():
    # Obtenemos la query de búsqueda desde la URL (?q=...)
    q = request.args.get("q", "").strip()

    conn = None
    cursor = None
    palabras = []

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        sql = """
            SELECT *
            FROM palabra_clave
            WHERE palabra ILIKE %s
               OR descripcion ILIKE %s
               OR respuesta_designada ILIKE %s
        """

        like = f"%{q}%"
        cursor.execute(sql, (like, like, like))
        palabras = cursor.fetchall()

    except Error as e:
        print(f"Error al buscar palabras clave: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Renderizamos la plantilla mostrando los resultados
    return render_template(
        "registros_crud/palabrasclave_tabla.html",
        palabras=palabras
    )
# ======================================================================================
@buscar_bp.route("/buscar-entradas")
def buscar_entradas():
    # 🔹 Obtener término de búsqueda de la URL (?q=algo)
    q = request.args.get("q", "").strip()

    conn = None
    cursor = None
    entradas = []

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # 🔹 Consulta con ILIKE para búsqueda insensible a mayúsculas
        sql = """
            SELECT *
            FROM diario_entrada
            WHERE titulo ILIKE %s
               OR contenido ILIKE %s
               OR estado::text ILIKE %s
               OR secretaria_responsable ILIKE %s
        """
        like = f"%{q}%"
        cursor.execute(sql, (like, like, like, like))
        entradas = cursor.fetchall()

    except Error as e:
        print(f"Error al buscar entradas de diario: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # 🔹 Renderizar resultados en tu plantilla de entradas
    return render_template(
        "registros_crud/entradasdiario_tabla.html",
        entradas=entradas,
        termino=q
    )
# ======================================================================================
@buscar_bp.route("/buscar-conversaciones")
def buscar_conversaciones():
    q = request.args.get("q", "").strip()  # Lo que el usuario escribe en el buscador

    conn = None
    cursor = None
    resultados = []

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        sql = """
            SELECT *
            FROM conversacion
            WHERE id_conversacion::TEXT ILIKE %s   -- CAST a TEXT para buscar números
               OR cedula_solicitante ILIKE %s
        """

        like = f"%{q}%"
        cursor.execute(sql, (like, like))
        resultados = cursor.fetchall()

    except Error as e:
        print(f"Error al buscar conversaciones: {e}")
        resultados = []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/conversaciones_tabla.html",
        conversaciones=resultados
    )
# ======================================================================================
@buscar_bp.route("/buscar-secretaria")
def buscar_secretaria():
    q = request.args.get("q", "").strip()

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        sql = """
            SELECT *
            FROM admin_secretaria
            WHERE cedula   ILIKE %s
               OR nombre   ILIKE %s
               OR apellido ILIKE %s
        """

        like = f"%{q}%"
        cursor.execute(sql, (like, like, like))
        resultados = cursor.fetchall()

    except Error as e:
        print(f"Error al buscar secretarias: {e}")
        resultados = []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/secretaria_tabla.html",
        secretarias=resultados
    )
# ======================================================================================