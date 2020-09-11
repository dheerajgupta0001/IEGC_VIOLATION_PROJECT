'''
This is the web server that acts as a service that creates raw pair angle separations data
'''
import datetime as dt
from src.config.appConfig import getConfig
from src.fetchers.significanceViolationFetcher import fetchIegcViolationData
from src.repos.insertViolationData import IegcViolationSummaryRepo
from flask import Flask, request, jsonify
from src.typeDefs.appConfig import IAppConfig

app = Flask(__name__)

# get application config
appConfig: IAppConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']
iegcMessageFolderPath = appConfig['violationDataFolder']
appDbConnStr = appConfig['appDbConStr']


@app.route('/')
def hello():
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