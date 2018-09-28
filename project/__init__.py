from flask import  Flask,url_for,render_template

app=Flask(__name__)

app.secret_key=b'\xfc\xc0\x8a0<~\x1d\x1c\x98o\xf1\x7fZQ \xd7\x0c\x9cy\x14\x14\xc2\xe4\r'


from project.views import home
from project.views import backend

app.register_blueprint(home.mod)
app.register_blueprint(backend.mod)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 400

@app.url_defaults
def add_language_code(endpoint,values):
    pass

@app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    pass
