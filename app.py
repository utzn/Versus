from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/login')
def home():
    errors = []
    results = []
    try:
        login_form = request.form["login_data"]

    except:
        errors.append()

    return render_template("home.html", errors=errors, results=results)


if __name__ == '__main__':
    app.run()
