################################################################################################
################################################################################################
from flask import Blueprint, render_template, request, redirect, flash
from database.db import get_db
from database.db import get_db
from psycopg2.extras import RealDictCursor
from psycopg2 import Error

palabrasclave_formulario_bp = Blueprint("palabrasclave_formulario_bp",__name__)

# ======================================================
# 2. TRAER INFORMACION DE EDICIÓN
# ======================================================
@palabrasclave_formulario_bp.route("/editar-palabraclave/<id_pc>", methods=["GET"])
def traerinformacion(id_pc):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # GET → llenar formulario
        cursor.execute("""
            SELECT *
            FROM palabra_clave
            WHERE id_pc = %s
        """, (id_pc,))

        pc_editar = cursor.fetchone()

    except Error as e:
        print(f"Error al obtener secretaria: {e}")
        pc_editar = None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "editables/palabrasclave_editar.html",
        pc_editar=pc_editar
    )
################################################################################################
################################################################################################