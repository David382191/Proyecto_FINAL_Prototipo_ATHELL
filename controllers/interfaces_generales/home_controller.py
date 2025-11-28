from flask import Blueprint, render_template

home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/consultantes")
def panel_consultantes():
    return render_template("panel_consultantes.html")

@home_bp.route("/administradores")
def panel_administradores():
    return render_template("registro-admin.html")

@home_bp.route("/conversaciones")
def panel_conversaciones():
    return render_template("panel_conversaciones.html")

@home_bp.route("/palabras-clave")
def panel_palabras_clave():
    return render_template("panel_palabras_clave.html")

@home_bp.route("/salir")
def salir():
    return render_template("login.html")

@home_bp.route("/ejercicio-adicional")
def ejercicio_adicional():
    return render_template("config_avanzada.html")
