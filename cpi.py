from app import app
import os

if __name__ == 'main':
    app.run(threaded=True)
    port = int(os.getenv('PORT'), '5000')
    app.run(host='0.0.0.0', port = port)
    