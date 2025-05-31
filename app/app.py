from flask import Flask
from routers.v1.api import api_router
from routers.v1.fatigue import api_fatigue_router

app = Flask(__name__)
app.register_blueprint(api_router)
app.register_blueprint(api_fatigue_router)


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
