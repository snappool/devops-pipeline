"""A tiny Flask app. The app itself is simple on purpose:
the learning is in the pipeline built around it."""
import os

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(message="Hello from the DevOps pipeline!", version=os.getenv("APP_VERSION", "dev"))


@app.route("/health")
def health():
    # Docker, Kubernetes and load balancers call an endpoint like this
    # to check whether the app is alive.
    return jsonify(status="ok")


@app.route("/greet")
def greet():
    name = request.args.get("name", "world")
    return jsonify(greeting=f"Hello, {name}!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
