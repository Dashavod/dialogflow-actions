# import flask dependencies
from flask import Flask, request
from service import Service

# initialize the flask app
app = Flask(__name__)
service = Service()
# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    fulfillmentText = ''
    query_result = req.get('queryResult')
    match query_result.get('action'):
        case 'get.orbit_planet': fulfillmentText = service.OrbitPlanet(query_result)
        case 'get.info_planet': fulfillmentText = service.InfoPlanet(query_result)
        case 'get.cosmo_question':fulfillmentText = service.RadiusPlanet(query_result)
        case 'get.comparsion_planet': fulfillmentText = service.ComparsionPlanet(query_result)
    return {
            "fulfillmentText": fulfillmentText,
            "source": "webhookdata"
        }
@app.route('/')
def response():
    return "hello"

# run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0')

