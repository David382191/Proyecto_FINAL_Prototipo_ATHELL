#################################################################################################
#################################################################################################

from flask import Flask

# IMPORTAR BLUEPRINTS (tiene que ser uno por carpeta)

# ----------------------------- FORMULARIOS -------------------------------------------------#
from controllers.formularios.secretaria_formulario_controller import secretaria_form_bp
from controllers.formularios.palabrasclave_formulario_controller import palabras_form_bp
from controllers.formularios.solicitante_formulario_controller import solicitante_form_bp

# ----------------------- INTERFACES GENERALES ----------------------------------------------#
from controllers.interfaces_generales.home_controller import home_bp
from controllers.interfaces_generales.panel_controller import panel_bp

# ------- CRUD (Donde nos sale la tabla de registros y en algunos casos pocos botones) -----#
from controllers.registro_crud.consultantes_tabla_controller import consultantes_bp
from controllers.registro_crud.conversaciones_tabla_controller import conversaciones_bp
from controllers.registro_crud.mensajes_tabla_controller import mensajes_bp
from controllers.registro_crud.palabrasclave_tabla_controller import palabrasclave_bp
from controllers.registro_crud.secretaria_tabla_controller import secretarias_bp


app = Flask(__name__)
app.secret_key = "ATHELL_SECRET_KEY_999"


# -------------- REGISTRO DE BLUEPRINTS -------------- #

# Formularios
app.register_blueprint(secretaria_form_bp)
app.register_blueprint(palabras_form_bp)
app.register_blueprint(solicitante_form_bp)

# Interfaces generales
app.register_blueprint(home_bp)
app.register_blueprint(panel_bp)

# Tablas CRUD
app.register_blueprint(consultantes_bp)
app.register_blueprint(conversaciones_bp)
app.register_blueprint(mensajes_bp)
app.register_blueprint(palabrasclave_bp)
app.register_blueprint(secretarias_bp)


# ------------------- EJECUCIÓN --------------------- #
if __name__ == "__main__":
    app.run(debug=True)

#################################################################################################
#################################################################################################