# import flask dependencies
from flask import Flask, request
from service import Service

# initialize the flask app
app = Flask(__name__)
service = Service()
user_info = {}

index = 1


# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    global index

    req = request.get_json(silent=True, force=True)
    followupEvent = ''
    fulfillmentCards = ''
    query_result = req.get('queryResult')
    response = {"source": "webhookdata"}
    match query_result.get('action'):

        case "Benefits.Benefits-sport":
            fulfillmentCards = service.BenefitSportInfo(query_result)
            response["fulfillmentMessages"] = fulfillmentCards
        case 'actions.benefits':
            fulfillmentCards = service.BenefitGeneralInfo()
            response["fulfillmentMessages"] = fulfillmentCards
        case 'get.open_dialog_type1':
            fulfillmentCards = service.OpenDialogOneAnswer(query_result)
            response["fulfillmentMessages"] = fulfillmentCards
        case 'get.response_dialog_type1':
            fulfillmentCards = service.OneAnswer(query_result)
            response["fulfillmentMessages"] = fulfillmentCards
        case 'get.open_dialog_type2':
            fulfillmentCards = service.MultipleAnswer(query_result)
            response["fulfillmentMessages"] = fulfillmentCards
        case 'Quiz_type2.Quiz_type2-selectnumber':
            fulfillmentCards = service.ShowMultipleAnswer(query_result)
            response["fulfillmentMessages"] = fulfillmentCards
        case 'input.welcome':
            fulfillmentCards = chat_autorize(req)
            response["fulfillmentMessages"] = fulfillmentCards
        case 'get.url':
            fulfillmentCards = chat_card(req)
            response["fulfillmentMessages"] = fulfillmentCards
        case 'startquiz.startquiz-yes.startquiz-yes-custom.startquiz-yes-question-selectnumber':
            print(f"answer index {index}")
            fulfillmentCards = service.ShowMultipleAnswer(query_result, index)
            response["fulfillmentMessages"] = fulfillmentCards
        case 'startquiz.startquiz-yes.startquiz-yes-question':
            fulfillmentCards = service.DisplayQuestion(query_result)
            response["fulfillmentMessages"] = fulfillmentCards
        case 'startquiz.startquiz-yes.startquiz-yes-custom.startquiz-yes-question-input':
            fulfillmentCards = service.ShowInputAnswer(query_result, index)
            response["fulfillmentMessages"] = fulfillmentCards
        case 'input.unknown':
            fulfillmentCards = service.UnknownAnswer(req)
            response["fulfillmentMessages"] = fulfillmentCards
        case 'Ratebot.Ratebot-user':
            fulfillmentCards = service.UnknownAnswer(req)
            fulfillmentCards[0]["text"]['text'][0] = 'Thank you, I will remember your comment'
            response["fulfillmentMessages"] = fulfillmentCards
        case 'startquiz.startquiz-yes':
            print("yes intent")

            index = 1
            followupEvent = {
                "name": "open_question",
                "parameters": {
                    "number_of_question": index
                },
                "languageCode": "en-US"
            }
            response["followupEventInput"] = followupEvent
        case 'startquiz.startquiz-yes.startquiz-yes-custom.startquiz-yes-question-next':
            index += 1
            if index < 4:

                followupEvent = {
                    "name": "open_question",
                    "parameters": {
                        "number_of_question": index
                    },
                    "languageCode": "en-US"
                }
            else:
                index = 1
                followupEvent = {
                    "name": "close_quiz",
                    "parameters": {
                        "quantity_correct": service.quantity_correct
                    },
                    "languageCode": "en-US"
                }
            print(f"index =  {index}")

            response["followupEventInput"] = followupEvent
    print(response)
    return response


def chat_autorize(query_result):
    print(query_result)
    return [
        {
            "text": {
                "text": [
                    f"Hello {query_result['originalDetectIntentRequest']['payload']['data']['event']['user']['displayName']}"
                ]
            },
            "platform": "GOOGLE_HANGOUTS"
        },
        {
            "text": {
                "text": [
                    f"I'm a Devtorium-bot, I'm here to help you if you have any questions, choose from following category"
                ]
            },
            "platform": "GOOGLE_HANGOUTS"
        },
        {
            "platform": "GOOGLE_HANGOUTS",
            "payload": {
                "hangouts": {
                    "header": {
                        "title": "Choose category",
                        "subtitle": " "
                    },
                    "sections": [
                        {
                        "widgets": [
                            {
                                "keyValue": {
                                    "content": "holidays, structure, equipment,resources",
                                    "topLabel": "Company"
                                }
                            }
                        ]
                    },
                        {
                            "widgets": [
                                {
                                    "keyValue": {
                                        "content": "Sport,Health,Group activities,lunch,birth of a child,marriage,english classes",
                                        "topLabel": "Benefits"
                                    }
                                }
                            ]
                        },
                        {
                            "widgets": [
                                {
                                    "keyValue": {
                                        "content": "courses,certification, conferences, education resources",
                                        "topLabel": "Learning"
                                    }
                                }
                            ]
                        },

                    ],
                }
            }
        }
    ]


def chat_card(query_result):
    return [
        {
            "payload": {
                "hangouts": {
                    "header": {
                        "title": f"Hello {query_result['originalDetectIntentRequest']['payload']['data']['event']['user']['displayName']}",
                    },
                    "sections": [
                        {
                            "widgets": [{
                                "image": {
                                    "imageUrl":
                                        query_result['originalDetectIntentRequest']['payload']['data']['event']['user'][
                                            'avatarUrl']
                                }
                            }]
                        }]
                }
            },
            "platform": "GOOGLE_HANGOUTS"
        }
    ]


####### try for OAuth
import os
import flask
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = scopes = ['openid', 'https://www.googleapis.com/auth/userinfo.email',
                   'https://www.googleapis.com/auth/userinfo.profile']
# API_SERVICE_NAME = 'people'
# API_VERSION = 'v1'

# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.
app.secret_key = 'REPLACE ME - this value is here as a placeholder.'


@app.route('/')
def index():
    return print_index_table()


@app.route('/test')
def test_api_request():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    user_info_service = googleapiclient.discovery.build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
    print(user_info['email'])
    # res = googleapiclient.discovery.build(
    #      API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # results = res.execute()
    # print(results)
    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.jsonify(**user_info)


@app.route('/authorize')
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='false')

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']
    print(f"callback {state}")
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    print(flask.request.url)
    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    print(authorization_response)
    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('test_api_request'))


@app.route('/revoke')
def revoke():
    if 'credentials' not in flask.session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
                'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    revoke = requests.post('https://oauth2.googleapis.com/revoke',
                           params={'token': credentials.token},
                           headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return ('Credentials successfully revoked.' + print_index_table())
    else:
        return ('An error occurred.' + print_index_table())


@app.route('/clear')
def clear_credentials():
    if 'credentials' in flask.session:
        del flask.session['credentials']
    return ('Credentials have been cleared.<br><br>' +
            print_index_table())


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def print_index_table():
    return ('<table>' +
            '<tr><td><a href="/test">Test an API request</a></td>' +
            '<td>Submit an API request and see a formatted JSON response. ' +
            '    Go through the authorization flow if there are no stored ' +
            '    credentials for the user.</td></tr>' +
            '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
            '<td>Go directly to the authorization flow. If there are stored ' +
            '    credentials, you still might not be prompted to reauthorize ' +
            '    the application.</td></tr>' +
            '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
            '<td>Revoke the access token associated with the current user ' +
            '    session. After revoking credentials, if you go to the test ' +
            '    page, you should see an <code>invalid_grant</code> error.' +
            '</td></tr>' +
            '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
            '<td>Clear the access token currently stored in the user session. ' +
            '    After clearing the token, if you <a href="/test">test the ' +
            '    API request</a> again, you should go back to the auth flow.' +
            '</td></tr></table>')


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.

    app.run(host='0.0.0.0')
