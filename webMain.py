from Controller import app, DownloadController

if __name__ == '__main__':
    #Globals.app.debug = True

    DownloadController.socketio.run(app, host='0.0.0.0', use_reloader=False)
