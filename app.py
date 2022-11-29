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
    fulfillmentCards = ''
    query_result = req.get('queryResult')
    match query_result.get('action'):
        case 'get.orbit_planet': fulfillmentCards = service.OrbitPlanet(query_result)
        case 'get.info_planet': fulfillmentCards = service.InfoPlanet(query_result)
        case 'get.cosmo_question': fulfillmentCards = service.RadiusPlanet(query_result)
        case 'get.comparsion_planet': fulfillmentCards = service.ComparsionPlanet(query_result)
        case 'get.test_card': fulfillmentCards = service.TestCard(query_result)
        case 'get.open_dialog_type1': fulfillmentCards = service.OpenDialogOneAnswer(query_result)
        case 'get.response_dialog_type1': fulfillmentCards = service.OneAnswer(query_result)
        case 'get.open_dialog_type2': fulfillmentCards = service.MultipleAnswer(query_result)
    return {
        "fulfillmentMessages": fulfillmentCards,

        "source": "webhookdata"
    }
@app.route('/')
def response():
    return "hello"

# run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0')

