from app import app
import GetData, schedule, time, os

def jobFive():
    GetData.BasicData.variacoes()

if __name__ == 'main':

    schedule.every(5).minutes.do(jobFive)

    app.debug = True
    app.run(threaded=True)
    port = int(os.getenv('PORT'), '5000')
    app.run(host='0.0.0.0', port = port)
    
    while True:
        schedule.run_pending()
        time.sleep(2)
