#################################################################################################
#################################################################################################
from flask import Flask, redirect, render_template

# IMPORTAR BLUEPRINTS (tiene que ser uno por carpeta)
# ----------------------------- FORMULARIOS -------------------------------------------------#
from controllers.formularios.secretaria_formulario_controller import secretaria_form_bp
from controllers.formularios.palabrasclave_formulario_controller import palabrasclave_formulario_bp
from controllers.formularios.solicitante_formulario_controller import solicitante_form_bp

# ----------------------- INTERFACES GENERALES ----------------------------------------------#
from controllers.interfaces_generales.home_controller import home_bp
from controllers.interfaces_generales.login_controller import login_bp

# ------- CRUD (Donde nos sale la tabla de registros y en algunos casos pocos botones) -----#
from controllers.registro_crud.solicitante_tabla_controller import solicitantes_bp
from controllers.registro_crud.conversaciones_tabla_controller import conversaciones_bp
from controllers.registro_crud.mensajes_tabla_controller import mensajes_bp
from controllers.registro_crud.palabrasclave_tabla_controller import palabras_bp
from controllers.registro_crud.secretaria_tabla_controller import secretaria_bp

# ----------------------- Editables ----------------------------------------------#
from controllers.editables.editar import editar

def create_app():
    app = Flask(__name__)
    app.secret_key = "ATHELL_SECRET_KEY_999"

    # -------------- REGISTRO DE BLUEPRINTS -------------- #

    # Formularios
    #app.register_blueprint(secretaria_form_bp)
    app.register_blueprint(palabrasclave_formulario_bp)
    app.register_blueprint(solicitante_form_bp)

    # Interfaces generales
    app.register_blueprint(home_bp)
    app.register_blueprint(login_bp)

    # Tablas CRUD
    app.register_blueprint(solicitantes_bp)
    app.register_blueprint(conversaciones_bp)
    app.register_blueprint(mensajes_bp)
    app.register_blueprint(palabras_bp)
    app.register_blueprint(secretaria_bp)

    #Editar
    app.register_blueprint(editar)

    return app

#################################################################################################
if __name__ == "__main__":
    app = create_app()
    #print(app.url_map)  
    app.run(debug=True)
#################################################################################################
#Así ya no dan ganas de suicidarse... aún...pero lo sigo teniendo en la agenda.
#    print("RUTAS REGISTRADAS:")
#    print(app.url_map)