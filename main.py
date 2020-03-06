from flask import Flask

app = Flask(__name__)


@app.route('/', methods=["GET"])
def main():
    return "test"



application = app # gunicorn requires main.py to contain application
if __name__ == '__main__':
    application.run(debug=True, port=5000, host='0.0.0.0')