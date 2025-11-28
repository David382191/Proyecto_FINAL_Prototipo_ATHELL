from flask import Flask
from controllers.registro_secretaria_routers import secretarias

app = Flask(__name__)
app.secret_key = "123"

app.register_blueprint(secretarias)

if __name__ == "__main__":
    app.run(debug=True)
