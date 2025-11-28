# test_secretaria.py

from flask import Flask
from controllers.registro_secretaria_routers import secretarias  # <--- CORRECTO

app = Flask(__name__)
app.secret_key = "testing123"

app.register_blueprint(secretarias)

if __name__ == "__main__":
    print("\n🔥 Servidor de prueba iniciado en: http://localhost:5000/crear-secretaria\n")
    app.run(debug=True)
