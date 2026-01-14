############################################################################################
############################################################################################
from flask import Blueprint, render_template, flash, request, redirect
from mysql.connector import Error
from database.db import get_db

secretaria_bp = Blueprint('secretaria_bp', __name__)


# ============================================================
# LISTAR TODAS LAS SECRETARIAS
# ============================================================
@secretaria_bp.route("/lista_secretarias")
def lista_secretarias():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # 1️⃣ ¿Qué base de datos es?
    cursor.execute("SELECT DATABASE()")
    print("📌 BASE DE DATOS:", cursor.fetchone())

    # 2️⃣ ¿Cuántos registros hay?
    cursor.execute("SELECT COUNT(*) AS total FROM admin_secretaria")
    print("📌 TOTAL REGISTROS:", cursor.fetchone())

    # 3️⃣ Traer datos reales
    cursor.execute("""
        SELECT
            cedula   AS CEDULA,
            nombre   AS Nombre,
            apellido AS Apellido,
            usuario  AS Usuario,
            telefono AS Telefono
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
# 2. BUSCAR SOLICITANTE (por nombre / cedula / tipo)
# ============================================================
@secretaria_bp.route("/buscar-secretaria")
def buscar_secretaria():
    q = request.args.get("q", "")

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT * FROM admin_secretaria
        WHERE cedula LIKE %s
           OR nombre LIKE %s
           OR apellido LIKE %s
    """

    like = f"%{q}%"
    cursor.execute(sql, (like, like, like))
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "registros_crud/secretaria_tabla.html",
        secretarias=resultados
    )


# ============================================================
# 3. EDITAR SOLICITANTE (GET + POST)
# ============================================================
@secretaria_bp.route("/editar-secretaria/<cedula>", methods=["GET", "POST"])
def editar_solicitante(cedula):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        tipo = request.form["tipo"]

        sql = """
            UPDATE admin_secretaria
            SET Nombre=%s, Telefono=%s, Tipo_solicitante=%s
            WHERE CEDULA=%s
        """
        cursor.execute(sql, (nombre, telefono, tipo, cedula))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect("/solicitantes")

    # GET → llenar formulario
    cursor.execute("SELECT * FROM admin_secretaria WHERE CEDULA=%s", (cedula,))
    solicitante = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("formularios/secretaria_formulario.html", solicitante=solicitante)


############################################################################################
############################################################################################