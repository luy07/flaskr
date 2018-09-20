from flask import Blueprint,url_for,render_template,make_response,session,Markup

mod=Blueprint('backend',__name__,url_prefix='/backend')

@mod.route('/')
@mod.route('/index')
def index():
    tmpt = Markup.escape(u'<strong>Hello %s!</strong>' % '<blink>hacker</blink>')

    content= render_template('backend/index.html',tmpt=tmpt)
    resp=make_response(content)
    resp.set_cookie('username','luy')
    return  resp

@mod.route('/users')
def user_management():
    url= url_for('.index')
    session['username']='luyq'
    return render_template('backend/user_management.html',url=url)

