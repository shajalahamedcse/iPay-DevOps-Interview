from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/ping')
def hello():
    return 'pong'


@app.route('/reverse', methods=['POST'])
def hello_world():
    data = request.get_json()
    app.logger.info(data)
    message = data.get('message')
    message = reverse_slicing(message)
    response_object = {
        'message': message,
    }
    app.logger.info(response_object)
    return jsonify(response_object)


def reverse_slicing(s):
    return s[::-1]


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
