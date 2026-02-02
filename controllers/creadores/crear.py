from flask import Blueprint, request, render_template, redirect, flash, url_for
from psycopg2.extras import RealDictCursor
from psycopg2 import Error
from database.db import get_db
crear_bp = Blueprint("crear_bp",__name__)
#################################################################################################
@crear_bp.route("/crear-palabra", methods=["GET", "POST"])
def crear_palabra_clave():
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        if request.method == "POST":

            # 🔴 VALIDACIÓN
            palabra = request.form.get("palabra", "").strip()
            descripcion = request.form.get("descripcion", "").strip()
            respuesta = request.form.get("respuesta", "").strip()

            if not palabra or not respuesta:
                flash("Palabra y respuesta son obligatorias", "danger")
                return redirect(request.url)

            # 🟢 INSERT
            cursor.execute("""
                INSERT INTO palabra_clave (palabra, descripcion, respuesta_designada)
                VALUES (%s, %s, %s)
            """, (palabra, descripcion, respuesta))

            conn.commit()
            flash(f"Palabra '{palabra}' agregada correctamente", "success")
            return redirect(url_for("palabras_bp.guardar_palabra"))

    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error al crear palabra clave: {e}")
        flash("Error al registrar la palabra clave", "danger")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # ✅ Renderiza el formulario
    return render_template("registro_crud/palabrasclave_tabla.html")
#######################################################################################