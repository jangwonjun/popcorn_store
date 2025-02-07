from flask import Flask, render_template, request, make_response
from requests.auth import HTTPBasicAuth
import requests
import uuid
import json

clientId = 'S1_f23eac193e4a4a0f8efbb800439e62d9'
secretKey = '4dcbf5bfe58d498c95095f1cea381596'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        orderId = uuid.uuid4(),
        clientId = clientId
    )

    
@app.route('/cancel', methods=['GET'])
def cancel():
    return render_template(
        'cancel.html'
    )    


@app.route('/clientAuth', methods=['POST'])
def clientAuth():
    print(request.form)
    return render_template(
        'response.html',
        resultMsg = request.form['resultMsg']
    )


@app.route('/cancel', methods=['POST'])
def cancelAuth():
    try:
        response = requests.post('https://sandbox-api.nicepay.co.kr/v1/payments/'+ request.form['tid'] + '/cancel', 
            json={
                'amount': request.form['amount'],
                'reason' : 'test',
                'orderId' : str(uuid.uuid4())
            },
            headers={
                'Content-type' : 'application/json'
            },
            auth=HTTPBasicAuth(clientId, secretKey)
        )
        
        resDict = json.loads(response.text)
        print(resDict)
        
        # 결제 비즈니스 로직 구현
        
        return render_template(
            'response.html',
            resultMsg = resDict['resultMsg']
        )
        
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


@app.route('/hook', methods=['POST'])
def hook():
    print(request.json)
    return make_response("ok", 200)


if __name__ == '__main__':
    app.run(debug=True)