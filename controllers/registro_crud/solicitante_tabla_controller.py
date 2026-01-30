from flask import request, render_template
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from database.db import get_db


solicitantes_bp = Blueprint("solicitantes_bp", __name__)

# ============================================================
@solicitantes_bp.route('/home')
def home():
    return render_template('interfaces_generales/home.html')
# ============================================================
@solicitantes_bp.route('/crud_solicitantes')
def crud_solicitantes():
    return render_template('registros_crud/solicitantes_tabla.html')
# ============================================================


# ============================================================
# 1. LISTAR SOLICITANTES
# ============================================================
@solicitantes_bp.route("/registros_crud/solicitantes_tabla")
def listar_solicitantes():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM SOLICITANTE")
    solicitantes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("registros_crud/solicitantes_tabla.html", solicitantes=solicitantes)

# ============================================================
# 2. BUSCAR SOLICITANTE (por nombre / cedula / tipo)
# ============================================================
@solicitantes_bp.route("/buscar-solicitante")
def buscar_solicitante():
    q = request.args.get("q", "")

    conn = None
    cursor = None
    resultados = []

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        sql = """
            SELECT * FROM solicitante
            WHERE cedula LIKE %s OR nombre LIKE %s OR tipo_solicitante LIKE %s
        """
        like = f"%{q}%"
        cursor.execute(sql, (like, like, like))
        resultados = cursor.fetchall()

    except Error as e:
        print(f"Error al buscar solicitantes: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "registros_crud/solicitantes_tabla.html",
        solicitantes=resultados
    )
# ============================================================
# 3. ELIMINAR SOLICITANTE
# ============================================================

@solicitantes_bp.route("/eliminar-solicitante/<cedula>")
def eliminar_solicitante(cedula):

    if not eliminar_solicitante_si_es_posible(cedula):
        flash(
            "No se puede eliminar el solicitante porque tiene conversaciones asociadas",
            "danger"
        )
        return redirect(url_for("home_bp.panel_solicitantes"))

    flash("Solicitante eliminado correctamente", "success")
    return redirect(url_for("home_bp.panel_solicitantes"))

#####............................................................
def eliminar_solicitante_si_es_posible(cedula):
    print(">>> CEDULA RECIBIDA:", cedula)

    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor()  # no necesitamos RealDictCursor aquí, solo contaremos

        # Revisar si tiene conversaciones
        cursor.execute(
            "SELECT COUNT(*) FROM conversacion WHERE cedula_solicitante = %s",
            (cedula,)
        )
        total = cursor.fetchone()[0]
        print(">>> CONVERSACIONES:", total)

        if total > 0:
            print(">>> NO SE ELIMINA")
            return False

        # Eliminar solicitante
        cursor.execute(
            "DELETE FROM solicitante WHERE cedula = %s",
            (cedula,)
        )
        conn.commit()
        print(">>> ELIMINADO")
        return True

    except Error as e:
        print(f"Error al eliminar solicitante: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ============================================================
# 5. TRAER INFORMACIÒN SOLICITANTE
# ============================================================
@solicitantes_bp.route("/editar-solicitante/<cedula>", methods=["GET"])
def traerinformacion(cedula):
    conn = None
    cursor = None
    solicitante_editar = None

    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # GET → llenar formulario
        cursor.execute("SELECT * FROM solicitante WHERE cedula = %s", (cedula,))
        solicitante_editar = cursor.fetchone()

    except Error as e:
        print(f"Error al traer información del solicitante: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    print("CEDULA RECIBIDA:", cedula)
    print("SOLICITANTE:", solicitante_editar)

    return render_template(
        "editables/solicitante_editar.html",
        solicitante_editar=solicitante_editar
    )
# ============================================================