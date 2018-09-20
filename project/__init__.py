from flask import  Flask,url_for,render_template

app=Flask(__name__)

app.secret_key=b'\xfc\xc0\x8a0<~\x1d\x1c\x98o\xf1\x7fZQ \xd7\x0c\x9cy\x14\x14\xc2\xe4\r'



from project.views import home
from project.views import backend

app.register_blueprint(home.mod)
app.register_blueprint(backend.mod)

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route("/sitemap")
def site_map():
    links=[]
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return render_template('backend/sitemap.html', sitelinks=links)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 400

