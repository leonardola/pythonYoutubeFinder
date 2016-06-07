from flask import render_template
from Controller import app, database, getRequestData

@app.route('/')
def home():
    return render_template('home.html.jinja2', download_path = database.get_download_path())

@app.route('/updateDownloadPath', methods = ["POST"])
def update_download_path():
    data = getRequestData()

    database.set_download_path(data['newDownloadPath'])
    return "ok"