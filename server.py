'''
This is the web server that acts as a service that creates raw/derived data of voltage and frequency
'''
import datetime as dt
from src.config.appConfig import getConfig
from src.fetchers.significanceViolationFetcher import fetchIegcViolationData, getIegcViolationMsgsFilePath
from src.repos.insertViolationData import IegcViolationSummaryRepo
from src.typeDefs.iegcViolationSummary import IViolationMessageSummary
from src.dataFetcher.iegcViolMsgsFetcher import IegcViolMsgsFetcher
from flask import Flask, request, jsonify

app = Flask(__name__)

# get application config
appConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']

appDbConnStr = appConfig['appDbConStr']


@app.route('/')
def hello():
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


@app.route('/fetchIegcViolMsgs', methods=['GET'])
def fetchIegcViolMsgs():
    # get start and end dates from post request body
    try:
        startDateStr = request.args.get('startDate', None, type=str)
        endDateStr = request.args.get('endDate', None, type=str)
        startDate = dt.datetime.strptime(startDateStr, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDateStr, '%Y-%m-%d')
    except Exception as ex:
        return jsonify({'message': 'Unable to parse start and end dates of this request body'}), 400

    try:
        # get iegc violation messages
        violMsgsFetcher = IegcViolMsgsFetcher(appDbConnStr)
        violMsgs: List[IIegcViolMsg] = violMsgsFetcher.fetchIegcViolMsgs(
            startDate, endDate)

        if violMsgs:
            return jsonify({'message': 'Success!!!', 'data': violMsgs, 'startDate': startDate, 'endDate': endDate})
        else:
            return jsonify({'message': 'IEGC violatiom message fetch unsuccessfull'}), 500
    except Exception as ex:
        return jsonify({'message': 'some error occured...'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(appConfig['flaskPort']), debug=True)
