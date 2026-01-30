from flask import Blueprint, render_template, request, redirect, flash
from psycopg2.extras import RealDictCursor
from database.db import get_db
from psycopg2 import Error

palabras_bp = Blueprint("palabras_bp", __name__)

# ======================================================
# LISTAR PALABRAS
# ======================================================
@palabras_bp.route("/registros_crud/palabrasclave_tabla")
def listar_palabras():
    conn = None
    cursor = None
    palabras = []

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Obtener todas las palabras
        cursor.execute("SELECT * FROM palabra_clave")
        palabras = cursor.fetchall()

    except Error as e:
        print(f"Error al listar palabras: {e}")
        palabras = []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/palabrasclave_tabla.html",
        palabras=palabras
    )
# ======================================================
# BUSCAR PALABRAS
# ======================================================
@palabras_bp.route("/buscar-palabras")
def buscar_palabras():
    query = request.args.get("q", "")

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT *
            FROM palabra_clave
            WHERE palabra ILIKE %s
               OR descripcion ILIKE %s
        """, (f"%{query}%", f"%{query}%"))

        palabras = cursor.fetchall()

    except Error as e:
        print(f"Error al buscar palabras clave: {e}")
        palabras = []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/palabrasclave_tabla.html",
        palabras=palabras
    )
# ======================================================
# FORMULARIO CREAR
# ======================================================
@palabras_bp.route("/palabras_clave", methods=["GET"])
def mostrar_tabla_palabras():
    return render_template("registros_crud/palabrasclave_tabla.html")
# ======================================================
# PROCESAR CREACIÓN
# ======================================================
@palabras_bp.route("/crear-palabra", methods=["POST"])
def guardar_palabra():
    palabra = request.form["Palabra"]
    descripcion = request.form["Descripcion"]
    respuesta = request.form["Respuesta_designada"]

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO palabra_clave (palabra, descripcion, respuesta_designada)
            VALUES (%s, %s, %s)
        """, (palabra, descripcion, respuesta))

        conn.commit()

    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error al guardar palabra clave: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect("/palabras")
# ======================================================
# FORMULARIO EDITAR
# ======================================================
@palabras_bp.route("/editar-palabra/<int:id_pc>")
def editar_palabra(id_pc):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT *
            FROM palabra_clave
            WHERE id_pc = %s
        """, (id_pc,))

        palabra = cursor.fetchone()

    except Error as e:
        print(f"Error al obtener palabra clave: {e}")
        palabra = None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "editar_palabra.html",
        palabra=palabra
    )
# ======================================================
# PROCESAR EDICIÓN
# ======================================================
@palabras_bp.route("/editar-palabra/<int:id_pc>", methods=["POST"])
def actualizar_palabra(id_pc):
    palabra = request.form["Palabra"]
    descripcion = request.form["Descripcion"]
    respuesta = request.form["Respuesta_designada"]

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE palabra_clave
            SET palabra = %s,
                descripcion = %s,
                respuesta_designada = %s
            WHERE id_pc = %s
        """, (palabra, descripcion, respuesta, id_pc))

        conn.commit()

    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error al actualizar palabra clave: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect("/palabras")
# ======================================================
# ELIMINAR
# ======================================================
@palabras_bp.route("/eliminar-palabra/<int:id_pc>")
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

    return redirect("/palabras")
#################################################################################################