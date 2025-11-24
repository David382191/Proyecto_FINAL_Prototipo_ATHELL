
from flask import Blueprint, render_template, session, redirect

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/usuarios")
def usuarios_panel():
    if "admin_id" not in session:
        return redirect("/")
    # Aquí luego podrías agregar lógica para consultar la base de datos
    return render_template("usuarios.html")
