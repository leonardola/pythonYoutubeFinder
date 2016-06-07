from flask import render_template, jsonify, request
from Controller import app, finder, database

@app.route("/channels")
def channels_page():
    channels = database.get_channels_list()
    return render_template("channels.html.jinja2", channels=channels)

@app.route("/channels/getDataByName/<channel_name>")
def get_channel_data_by_name(channel_name):
    data = finder.get_channels_with_name(channel_name)

    return jsonify(data=data)

@app.route("/getChannelData/<channel_id>")
def get_channel_data(channel_id):
    finder.get_channel_data(channel_id)

    return "ok"

@app.route("/channel/add", methods=["GET","POST"])
def add_channel():
    data = request.json
    database.save_channel(data)
    return "ok"

@app.route("/channel/remove/<channel_id>")
def remove_channel(channel_id):
    database.delete_channel_by_id(channel_id)
    return "ok"
