__author__ = 'leonardoalbuquerque'

from Controller import app, DownloadController

if __name__ == '__main__':
    app.debug = True
    DownloadController.socketio.run(app, use_reloader=True, host='0.0.0.0')