from flask import Blueprint, render_template, request, redirect
from database.db import get_conn

consultantes_bp = Blueprint("consultantes_bp", __name__)


# ============================================================
# 1. LISTAR SOLICITANTES
# ============================================================
@consultantes_bp.route("/consultantes")
def listar_solicitantes():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM SOLICITANTE")
    solicitantes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("registros_crud/consultantes_tabla.html", solicitantes=solicitantes)


# ============================================================
# 2. BUSCAR SOLICITANTE (por nombre / cedula / tipo)
# ============================================================
@consultantes_bp.route("/buscar-solicitante")
def buscar_solicitante():
    q = request.args.get("q", "")

    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT * FROM SOLICITANTE
        WHERE CEDULA LIKE %s OR Nombre LIKE %s OR Tipo_solicitante LIKE %s
    """
    
    like = f"%{q}%"
    cursor.execute(sql, (like, like, like))
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("registros_crud/consultantes_tabla.html", solicitantes=resultados)


# ============================================================
# 3. EDITAR SOLICITANTE (GET + POST)
# ============================================================
@consultantes_bp.route("/editar-solicitante/<cedula>", methods=["GET", "POST"])
def editar_solicitante(cedula):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        tipo = request.form["tipo"]

        sql = """
            UPDATE SOLICITANTE
            SET Nombre=%s, Telefono=%s, Tipo_solicitante=%s
            WHERE CEDULA=%s
        """
        cursor.execute(sql, (nombre, telefono, tipo, cedula))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect("/consultantes")

    # GET → llenar formulario
    cursor.execute("SELECT * FROM SOLICITANTE WHERE CEDULA=%s", (cedula,))
    solicitante = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("formularios/solicitante_formulario.html", solicitante=solicitante)


# ============================================================
# 4. ELIMINAR SOLICITANTE
# ============================================================
@consultantes_bp.route("/eliminar-solicitante/<cedula>")
def eliminar_solicitante(cedula):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM SOLICITANTE WHERE CEDULA=%s", (cedula,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/consultantes")

#### mecachis, consultantes y solicitantes son lo mismo, me equivoqué de nombre.
