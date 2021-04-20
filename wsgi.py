"""App entry point."""
from app import init_app, init_client_app

app = init_app()
client_app = init_client_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    client_app.run(host="0.0.0.0", port=6000)