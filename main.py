# import flask dependencies
from flask import Flask, request
from app import Service

# initialize the flask app
app = Flask(__name__)
service = Service()
# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    fulfillmentText = ''
    query_result = req.get('queryResult')
    if query_result.get('action') == 'get.orbit_planet':
        ### Perform set of executable code
        ### if required
        ### ...

        fulfillmentText = service.OrbitPlanet(query_result)
    if query_result.get('action') == 'get.info_planet':
        ### Perform set of executable code
        ### if required
        ### ...


        fulfillmentText = service.InfoPlanet(query_result)

    if query_result.get('action') == 'get.cosmo_question':
        ### Perform set of executable code
        ### if required
        ### ...

        fulfillmentText = service.RadiusPlanet(query_result)

    if query_result.get('action') == 'get.comparsion_planet':
        ### Perform set of executable code
        ### if required
        ### ...

        fulfillmentText = service.ComparsionPlanet(query_result)
    return {
            "fulfillmentText": fulfillmentText,
            "source": "webhookdata"
        }

# run the app
if __name__ == '__main__':
    app.run()

