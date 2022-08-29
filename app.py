from flask import Flask, session, redirect, render_template, url_for
import requests
import admin
import main
app = Flask(__name__)
app.config.update(
    SECRET_KEY='pGy5lNdVGMf6pGy5lNdVGMf6'
)
app.register_blueprint(main.mn)
app.register_blueprint(admin.adm)


@app.route('/')  # лавная страница
def index():
    if 'login' in session:  # if LOGIN in session - login it without questions
        return redirect(url_for('main_pages.logged'))
    return render_template('main.html')


if __name__ == "__main__":
    app.run()
