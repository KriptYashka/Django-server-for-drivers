from flask import Flask
from routers.v1.api import api_router

app = Flask(__name__)
app.register_blueprint(api_router)


@app.route("/")
def hello():
    return "Hello, World!"
