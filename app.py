from flask import Flask, render_template, request, redirect, url_for, flash, abort
import json
import os.path
from werkzeug.utils import secure_filename
#name of the module currently running in flask
app = Flask(__name__)
app.secret_key = 'h34ifeji359229040plf'


def load_urls():
    #read in the urls if they exist already
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            return json.load(urls_file)
    return None

@app.route('/')
def home():
    return render_template("home.html",name='Thomas')

@app.route('/your-url',methods=['GET','POST'])
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
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save("C:\\Users\\tkk10\\Documents\\Development\\Flask\\Flask_URL_Shortener\\static\\user_files\\" + full_name)
            urls[request.form['code']] = {'file': full_name}
        
        with open('urls.json','w') as url_file:
            json.dump(urls,url_file)

        return render_template("your_url.html",code=request.form['code'])
    else:
        return redirect(url_for('home'))

@app.route('/<string:code>')
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

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404