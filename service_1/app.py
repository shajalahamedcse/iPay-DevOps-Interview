from flask import Flask, jsonify, request
import random
import requests

app = Flask(__name__)
REV_URL = "http://servicetwo:5000/reverse"


@app.route('/ping')
def hello():
    return 'pong'


@app.route('/api', methods=['POST'])
def hello_world():
    data = request.get_json()
    message = data.get('message')
    revdata = {"message": message}

    try:
        res = requests.post(url=REV_URL, json=revdata)
        response_josn = res.json()
        app.logger.info(response_josn)
        message = response_josn.get('message')
    except requests.exceptions.HTTPError as e:
        app.logger.error(e.response)

    ran = random.uniform(0, 1)
    app.logger.info(ran)
    response_object = {
        'message': message,
        'rand': ran
    }
    app.logger.info(response_object)
    return jsonify(response_object)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
