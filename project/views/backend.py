from flask import Blueprint,url_for,render_template,make_response,session,Markup,current_app
from datamanager.datareader import stockreader

mod=Blueprint('backend',__name__,url_prefix='/backend')

@mod.route('/')
@mod.route('/index')
def index():
    tmpt = Markup.escape(u'<strong>Hello %s!</strong>' % '<blink>hacker</blink>')
    stocks=stockreader.get_all_stocks()
    content= render_template('backend/index.html',stocks=stocks[0:100])
    resp=make_response(content)
    resp.set_cookie('username','luy')
    return  resp

@mod.route('/users')
def user_management():
    url= url_for('.index')
    session['username']='luyq'
    return render_template('backend/user_management.html',url=url)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@mod.route("/sitemap")
def sitemap():
    links=[]
    for rule in current_app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return render_template('backend/sitemap.html', sitelinks=links)


