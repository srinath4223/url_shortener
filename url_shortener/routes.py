from flask import Blueprint, render_template, request, redirect

from .extensions import db
from .models import Link
from .auth import requires_auth

short = Blueprint('short', __name__)

@short.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()

    link.visits = link.visits + 1
    db.session.commit()

    return redirect(link.original_url) 

@short.route('/', methods = ['GET'])
@requires_auth
def index():
    return render_template('index.html') 



@short.route('/api', methods=['POST'])
@requires_auth
def add_link2():
    if request.form['submit_button'] == 'Register':
            original_url = request.form['original_url']
            link = db.session.query(Link).filter(Link.original_url == original_url).first()
            if link:
                short_url= link.short_url
                return render_template('link_already_present.html',original_url=original_url,short_url = short_url)
            else:
                link = Link(original_url=original_url)
                db.session.add(link)
                db.session.commit()
                return render_template('link_added2.html',new_link=link.short_url, original_url=link.original_url)
    elif request.form['submit_button'] == 'Delete':
            original_url = request.form['original_url']
            link = db.session.query(Link).filter(Link.original_url == original_url).first()
            if link:
                db.session.delete(link)
            db.session.commit()
            return render_template('link_deleted.html',deleted_link=original_url)
    elif request.form['submit_button'] == 'Update':
            original_url = request.form['original_url']
            link = db.session.query(Link).filter(Link.original_url == original_url).first()
            if link:
                short_url= link.short_url
                return render_template('link_update.html',original_url=original_url,short_url = short_url)
            else:
                return render_template('link_not_found.html')
    else:
            pass
            

@short.route('/update', methods=['POST'])
@requires_auth
def update():
    if request.form['submit_button'] == 'Update':
            original_url = request.form['original_url']
            updated_url = request.form['updated_url']
            link = db.session.query(Link).filter(Link.original_url == original_url).first()
            if link:
                link.original_url = updated_url
                db.session.commit()
            else:
                return render_template('link_not_found.html', original_url=link.original_url)
            return render_template('link_updated_success.html',updated_url=updated_url, original_url=original_url)
    else:
            pass
        
@short.route('/stats')
@requires_auth
def stats():
    links = Link.query.all()

    return render_template('stats.html', links=links)

@short.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404