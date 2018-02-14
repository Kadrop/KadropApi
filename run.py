from kadrop_api.app.api import app


if __name__ == "__main__":
    app.run("0.0.0.0", port=1234, debug=True)