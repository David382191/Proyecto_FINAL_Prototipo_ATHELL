###################################################################################################
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from database.db import get_db
from psycopg2.extras import RealDictCursor
from psycopg2 import Error
###################################################################################################
# Blueprint
editar = Blueprint("editar", __name__)
###################################################################################################
@editar.route("/editar/<cedula>", methods=["GET", "POST"])
def editarsecretaria(cedula):
    conn = None
    cursor = None
    secretaria_editar = None

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        if request.method == "POST":
            nombre = request.form["Nombre"]
            apellido = request.form["Apellido"]
            telefono = request.form["Telefono"]

            cursor.execute("""
                UPDATE admin_secretaria
                SET nombre   = %s,
                    apellido = %s,
                    telefono = %s
                WHERE cedula = %s
            """, (nombre, apellido, telefono, cedula))

            conn.commit()
            return redirect(url_for("home_bp.panel_administradores"))

        # GET → cargar datos
        cursor.execute("""
            SELECT *
            FROM admin_secretaria
            WHERE cedula = %s
        """, (cedula,))

        secretaria_editar = cursor.fetchone()

    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error al editar secretaria: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/secretaria_tabla.html",
        secretaria_editar=secretaria_editar
    )
######################################################################################
@editar.route("/editar-solicitante/<cedula>", methods=["GET", "POST"])
def editarsolicitante(cedula):
    conn = None
    cursor = None
    solicitante_editar = None

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        if request.method == "POST":
            nombre = request.form["Nombre"]
            cargo = request.form.get("Cargo")
            telefono = request.form["Telefono"]

            cursor.execute("""
                UPDATE solicitante
                SET nombre            = %s,
                    tipo_solicitante  = %s,
                    telefono          = %s
                WHERE cedula = %s
            """, (nombre, cargo, telefono, cedula))

            conn.commit()
            return redirect(url_for("home_bp.panel_solicitantes"))

        # GET → cargar datos
        cursor.execute("""
            SELECT *
            FROM solicitante
            WHERE cedula = %s
        """, (cedula,))

        solicitante_editar = cursor.fetchone()

    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error al editar solicitante: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/solicitantes_tabla.html",
        solicitante_editar=solicitante_editar
    )
######################################################################################
@editar.route("/editar-palabrasclave/<id_pc>", methods=["GET", "POST"])
def editar_pc(id_pc):
    conn = None
    cursor = None
    pc_editar = None

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        if request.method == "POST":
            palabra = request.form["palabra"]
            descripcion = request.form["descripcion"]
            respuesta_designada = request.form["respuesta_designada"]

            cursor.execute("""
                UPDATE palabra_clave
                SET palabra            = %s,
                    descripcion  = %s,
                    respuesta_designada          = %s
                WHERE id_pc = %s
            """, (palabra, descripcion, respuesta_designada, id_pc))

            conn.commit()
            return redirect(url_for("home_bp.panel_palabras_clave"))

        # GET → cargar datos
        cursor.execute("""
            SELECT *
            FROM palabra_clave
            WHERE id_pc = %s
        """, (id_pc,))

        pc_editar = cursor.fetchone()

    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error al editar Palabra Clave: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/palabrasclave_tabla.html",
        pc_editar=pc_editar
    )
######################################################################################
@editar.route("/editar-entradasdiario/<id_entrada>", methods=["GET", "POST"])
def editar_entradadiario(id_entrada):
    conn = None
    cursor = None
    entrada_editar = None

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        if request.method == "POST":
            titulo = request.form["titulo"]
            contenido = request.form["contenido"]
            estado = request.form["estado"]

            cursor.execute("""
                UPDATE diario_entrada
                SET titulo            = %s,
                    contenido  = %s,
                    estado          = %s
                WHERE id_entrada = %s
            """, (titulo, contenido, estado, id_entrada))

            conn.commit()
            return redirect(url_for("home_bp.entradasdiario"))

        # GET → cargar datos
        cursor.execute("""
            SELECT *
            FROM diario_entrada
            WHERE id_entrada = %s
        """, (id_entrada,))

        entrada_editar = cursor.fetchone()

    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error al editar Palabra Clave: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/entradasdiario_tabla.html",
        entrada_editar=entrada_editar
    )
######################################################################################
