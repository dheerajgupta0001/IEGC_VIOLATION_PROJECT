'''
<<<<<<< HEAD
This is the web server that acts as a service that creates raw pair angle separations data
'''
import datetime as dt
from src.config.appConfig import getConfig
from src.fetchers.significanceViolationFetcher import fetchIegcViolationData
from src.repos.insertViolationData import IegcViolationSummaryRepo
from flask import Flask, request, jsonify
from src.typeDefs.appConfig import IAppConfig
=======
This is the web server that acts as a service that creates raw/derived data of voltage and frequency
'''
import datetime as dt
from src.config.appConfig import getConfig
from src.fetchers.significanceViolationFetcher import fetchIegcViolationData, getIegcViolationMsgsFilePath
from src.repos.insertViolationData import IegcViolationSummaryRepo
from src.typeDefs.iegcViolationSummary import IViolationMessageSummary
from flask import Flask, request, jsonify
>>>>>>> 2a3cc70ba47f17cf3114a37e0b19993ad18f0645

app = Flask(__name__)

# get application config
<<<<<<< HEAD
appConfig: IAppConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']
iegcMessageFolderPath = appConfig['violationDataFolder']
=======
appConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']

>>>>>>> 2a3cc70ba47f17cf3114a37e0b19993ad18f0645
appDbConnStr = appConfig['appDbConStr']


@app.route('/')
def hello():
<<<<<<< HEAD
    return "This is the web server that acts as a service that creates iegc violation data"


@app.route('/iegc_violation_message', methods=['POST','GET'])
def createIegcMessage():
    reqData = request.get_json()
    
    iegcViolationData = fetchIegcViolationData(iegcMessageFolderPath)
        
    # get the instance of IEGC violation repository
    iegcDataRepo = IegcViolationSummaryRepo(appDbConnStr)
    # pushing iegc message Data to database
    isRawDataCreationSuccess = iegcDataRepo.pushViolationMessages(iegcViolationData)
    if isRawDataCreationSuccess:
        return jsonify({'message': 'iegc violation data creation successful!!!'})
    else:
        return jsonify({'message': 'iegc violation data creation was not success'}), 500


if __name__ == '__main__':
    app.run(debug=True)
=======
    return "This is the web service that acts as a service that creates iegc violation messages"


@app.route('/iegcViolMsgs', methods=['POST'])
def createIegcViolationMsgs():
    try:
        reqFile = request.files.get('inpFile')
        iegcViolationData = fetchIegcViolationData(reqFile)

        # get the instance of IEGC violation repository
        iegcDataRepo = IegcViolationSummaryRepo(appDbConnStr)
        # pushing IEGC violation messages to database
        isInsSuccess = iegcDataRepo.pushViolationMessages(iegcViolationData)

        if isInsSuccess:
            return jsonify({'message': 'IEGC Violation messages insertion successful!!!'})
    except Exception as ex:
        return jsonify({'message': 'some error occured...'}), 400
    return jsonify({'message': 'some error occured...'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(appConfig['flaskPort']), debug=True)
>>>>>>> 2a3cc70ba47f17cf3114a37e0b19993ad18f0645
