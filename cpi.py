from app import app
import os, time

if __name__ == 'main':
    app.debug = True
    app.run(threaded=True)
    port = int(os.getenv('PORT'), '5000')
    app.run(host='0.0.0.0', port = port)

