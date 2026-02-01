############################################################################################
############################################################################################
from flask import Blueprint, render_template, flash, request, redirect
from mysql.connector import Error
from database.db import get_db
from psycopg2.extras import RealDictCursor
from psycopg2 import Error
# ============================================================
secretaria_bp = Blueprint('secretaria_bp', __name__)
# ============================================================
# 1. LISTAR TODAS LAS SECRETARIAS
# ============================================================
@secretaria_bp.route("/lista_secretarias")
def lista_secretarias():
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # 1️⃣ ¿Qué base de datos es?
    cursor.execute("SELECT current_database() AS db")
    print("📌 BASE DE DATOS:", cursor.fetchone())

    # 2️⃣ ¿Cuántos registros hay?
    cursor.execute("SELECT COUNT(*) AS total FROM admin_secretaria")
    print("📌 TOTAL REGISTROS:", cursor.fetchone())

    # 3️⃣ Traer datos reales
    cursor.execute("""
        SELECT
            cedula   AS "cedula",
            nombre   AS "nombre",
            apellido AS "apellido",
            usuario  AS "usuario",
            telefono AS "telefono"
        FROM admin_secretaria
    """)
    secretarias = cursor.fetchall()
    print("📌 DATOS:", secretarias)

    cursor.close()
    conn.close()

    return render_template(
        "registros_crud/secretaria_tabla.html",
        secretarias=secretarias
    )
# ============================================================
# 2. BUSCAR SECRETARIA (por nombre / cedula / tipo)
# ============================================================
@secretaria_bp.route("/buscar-secretaria")
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
# ==========================
# 3. ELIMINAR SECRETARIA.
# ==========================
@secretaria_bp.route("/eliminar-secretaria/<cedula>")
def eliminar_secretaria(cedula):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM admin_secretaria
            WHERE cedula = %s
        """, (cedula,))

        conn.commit()

    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error al eliminar secretaria: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect("/secretaria_tabla")
# ==========================
#  4. TRAER INFORMACIÓN DE LA SECRETARIA
# ==========================
@secretaria_bp.route("/editar/<cedula>", methods=["GET"])
def traerinformacion(cedula):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # GET → llenar formulario
        cursor.execute("""
            SELECT *
            FROM admin_secretaria
            WHERE cedula = %s
        """, (cedula,))

        secretaria_editar = cursor.fetchone()

        print("CEDULA RECIBIDA:", cedula)
        print("SECRETARIA:", secretaria_editar)

    except Error as e:
        print(f"Error al obtener secretaria: {e}")
        secretaria_editar = None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "editables/secretaria_editar.html",
        secretaria_editar=secretaria_editar
    )
# =================================
#  5. IR A CREAR NUEVA SECRETARIA.
# =================================
@secretaria_bp.route("/ir-crear-secretaria", methods=["GET", "POST"])
def ir_crear_secretaria():
    
    return render_template("formularios/secretaria_formulario.html")
#    pass
############################################################################################
############################################################################################
##what does a men who is about to die think.
##It dopends. How he's going to die. Why he's dying.
## If he is going to kill himself.
## He may tought how here's nothing left for him.
## And hope there is something waiting for him in the other side.