from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify,Blueprint
import json
import os
from werkzeug.utils import secure_filename
from datetime import datetime

bp = Blueprint('urlshort',__name__)

def load_urls():
    #read in the urls if they exist already
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            return json.load(urls_file)
    return None
#home page route
@bp.route('/')
def home():
    return render_template("home.html",codes=session.keys())

@bp.route('/your-url',methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        #read in the urls if they exist already
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        #check to see if the code already exists in the urls dict
        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another!')
            return redirect(url_for('urlshort.home')) 

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            full_path = os.getcwd()
            if "Flask_URL_Shortener" not in full_path:
                full_path += "\\Flask_URL_Shortener\\urlshort\\static\\user_files\\"
            else:
                full_path += "\\urlshort\\static\\user_files\\"

            f.save(full_path + full_name)
            urls[request.form['code']] = {'file': full_name}
        with open('urls.json','w') as url_file:
            json.dump(urls,url_file)
            now = datetime.now()
            session[request.form['code']] = now.strftime("%d/%m/%Y %H:%M:%S")
        link = urls[request.form['code']] if "url" in urls[request.form['code']] else urls.get(request.form['code'])['file']
        return render_template("your_url.html",url_code=(request.form['code'],link))
    else:
        return redirect(url_for('urlshort.home'))

@bp.route('/<string:code>')
def redirect_to_url(code):
    urls = {}
    urls = load_urls()
    if urls:
        if code in urls.keys():
            if 'url' in urls[code].keys():
                return redirect(urls[code]['url'])
            else:
                return redirect(url_for('static',filename='/user_files/' + urls[code]['file']))
    
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404


@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
