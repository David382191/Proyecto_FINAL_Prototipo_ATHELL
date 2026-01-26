from flask import Blueprint, render_template, request, redirect
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

    conn = get_db()
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

    return render_template("registros_crud/solicitantes_tabla.html", solicitantes=resultados)

# ============================================================
# 3. ELIMINAR SOLICITANTE
# ============================================================
@solicitantes_bp.route("/eliminar-solicitante/<cedula>")
def registro_tiene_dependencias(conexion, tabla_padre, columna_pk, valor_pk):
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT TABLE_NAME, COLUMN_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE REFERENCED_TABLE_NAME = %s
          AND REFERENCED_COLUMN_NAME = %s
    """, (tabla_padre, columna_pk))

    dependencias = []

    for fk in cursor.fetchall():
        cursor.execute(
            f"SELECT COUNT(*) AS total FROM {fk['TABLE_NAME']} WHERE {fk['COLUMN_NAME']} = %s",
            (valor_pk,)
        )
        total = cursor.fetchone()["total"]

        if total > 0:
            dependencias.append({
                "tabla": fk["TABLE_NAME"],
                "columna": fk["COLUMN_NAME"],
                "total": total
            })

    cursor.close()
    return len(dependencias) > 0, dependencias

#### mecachis, solicitantes y solicitantes son lo mismo, me equivoqué de nombre.
# ============================================================
# 5. TRAER INFORMACIÒN SOLICITANTE
# ============================================================
@solicitantes_bp.route("/editar-solicitante/<cedula>", methods=["GET"])
def traerinformacion(cedula):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # GET → llenar formulario
    cursor.execute("SELECT * FROM SOLICITANTE WHERE CEDULA=%s", (cedula,))
    solicitante_editar = cursor.fetchone()

    cursor.close()
    conn.close()

    print("CEDULA RECIBIDA:", cedula)
    print("SECRETARIA:", solicitante_editar)

    return render_template("editables/solicitante_editar.html", solicitante_editar=solicitante_editar)

# ============================================================