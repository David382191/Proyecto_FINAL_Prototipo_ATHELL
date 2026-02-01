from flask import Blueprint, render_template, request, redirect, url_for, flash
from psycopg2.extras import RealDictCursor
from database.db import get_db
###################################################################################################
diario_bp = Blueprint("diario_bp", __name__)
###################################################################################################
@diario_bp.route("/lista_diario")
def listar_diario_tabla():
    conn = None
    cursor = None
    entradas = []

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT 
                id_entrada,
                fecha_creacion,
                titulo,
                estado,
                contenido,
                secretaria_responsable
            FROM diario_entrada
            ORDER BY fecha_creacion DESC
        """)

        entradas = cursor.fetchall()

    except Exception as e:
        print("Error al obtener diario:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/entradasdiario_tabla.html",
        entradas=entradas
    )
###################################################################################################
@diario_bp.route("/traer-entradadiario/<id_entrada>", methods=["GET"])
def traerinformacion(id_entrada):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # GET → llenar formulario
        cursor.execute("""
            SELECT *
            FROM diario_entrada
            WHERE id_entrada = %s
        """, (id_entrada,))

        entradasdiario_editar = cursor.fetchone()

    except Error as e:
        print(f"Error al obtener secretaria: {e}")
        entradasdiario_editar = None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "editables/entradasdiario_editar.html",
        entradasdiario_editar=entradasdiario_editar
    )
###################################################################################################