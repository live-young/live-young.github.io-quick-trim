from flask import Flask,render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'asfdv54vd51cv32c4z'

@app.route('/')
def home():
    return render_template('home.html', codes = session.keys())

@app.route('/your-url', methods = ['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        #to store short codes in json files
        if os.path.exists('urls.json'):
            with open('urls.json') as url_files:
                urls = json.load(url_files)

        #to check if short code exist already
        if request.form['code'] in urls.keys():
                flash('That short name already been taken. Please select another name.')
                return redirect(url_for('home'))

        #if link is url
        if 'url' in request.form.keys():
            urls[request.form['code']]= {'url': request.form['url']}

        #if link is file
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            #to avoid rubbish file names we use secure_filename method after importing secure_filename from werkzeug.utils
            f.save(r'D:\\Flask\\URL_shortner\\static\\user_files\\' + full_name)
            #to save files
            urls[request.form['code']]= {'file':full_name}

        with open('urls.json','w') as url_files:
            json.dump(urls,url_files)
            #saving in cookie/session info
            session[request.form['code']] = True
        return render_template('your_url.html', code= request.form['code'])
    else:
        return redirect(url_for('home'))

@app.route('/<string:code>') #for displaying the content using short codes
def redirect_to_url(code):
    #check url.json present
    if os.path.exists('urls.json'):
        with open('urls.json') as url_files:
            urls = json.load(url_files)
            #finding keys
            if code in urls.keys():
                #distinguish url and File
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url']) # gives url search
                #to see file we need to serve staric files, for this we made a static directory.
                #and inside this we made user_files specifically for the files uploaded by userfiles
                else: #for files redirection
                    return redirect(url_for('static', filename= 'user_files/'+ urls[code]['file']))
    return abort(404) #if file not exist we return 404

#design our error page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/api') #API conversion of the function
def session_api():
    return jsonify(list(session.keys()))


if(__name__ == '__main__'):
    app.run( debug = True)
