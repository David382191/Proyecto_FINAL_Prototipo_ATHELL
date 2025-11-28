#################################################################################################
#################################################################################################

from flask import Blueprint, render_template, request, redirect
from database.db import get_conn

solicitante_bp = Blueprint("solicitante_bp", __name__)


# ============================================================
# 1. LISTAR SOLICITANTES
# ============================================================
@solicitante_bp.route("/panel-consultantes")
def panel_solicitantes():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM SOLICITANTE")
    solicitantes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "registros_crud/consultantes_tabla.html",
        solicitantes=solicitantes
    )


# ============================================================
# 2. MOSTRAR FORMULARIO PARA MODIFICAR SOLICITANTE
# ============================================================
@solicitante_bp.route("/modificar-solicitante/<cedula>", methods=["GET"])
def mostrar_modificacion(cedula):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM SOLICITANTE WHERE CEDULA=%s", (cedula,))
    solicitante = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "formularios/modificar_solicitante.html",  # usa tu HTML
        solicitante=solicitante
    )


# ============================================================
# 3. GUARDAR CAMBIOS DE SOLICITANTE
# ============================================================
@solicitante_bp.route("/modificar-solicitante/<cedula>", methods=["POST"])
def guardar_modificacion(cedula):
    nombre = request.form["Nombre"]
    telefono = request.form["Telefono"]
    tipo = request.form["Tipo_solicitante"]

    conn = get_conn()
    cursor = conn.cursor()

    sql = """
        UPDATE SOLICITANTE
        SET Nombre=%s, Telefono=%s, Tipo_solicitante=%s
        WHERE CEDULA=%s
    """

    cursor.execute(sql, (nombre, telefono, tipo, cedula))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/panel-consultantes")


# ============================================================
# 4. ELIMINAR SOLICITANTE
# ============================================================
@solicitante_bp.route("/eliminar-solicitante/<cedula>")
def eliminar_solicitante(cedula):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM SOLICITANTE WHERE CEDULA=%s", (cedula,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/panel-consultantes")

#################################################################################################
#################################################################################################