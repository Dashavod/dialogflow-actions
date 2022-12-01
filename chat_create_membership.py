from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define your app's authorization scopes.
# When modifying these scopes, delete the file token.json, if it exists.
SCOPES = ["https://www.googleapis.com/auth/chat.memberships.app"]

def main():
    '''
    Authenticates with Chat API via user credentials,
    then adds the Chat app to a Chat space.
    '''

    # Start with no credentials.
    creds = None

    # Check for the file token.json. If it exists, use it for authentication.
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run in a file
        # named token.json.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build a service endpoint for Chat API.
    service = build('chat', 'v1', credentials=creds)

    # Set the Chat app as the entity that gets added to the space.
    # 'app' is an alias for the Chat app running the script.
    #
    # To specify a user, set:
    #
    # member = {
    #   'member': {
    #     'name':'users/{user}',
    #     'type':'HUMAN'
    #   }
    # }
    member = {
      'member': {
        'name':'users/app',
        'type': 'BOT'
      }
    }

    # Use the service endpoint to call Chat API.
    result = service.spaces().members().create(

      # Replace {space} with a space name.
      # Obtain the space name from the spaces resource of Chat API,
      # or from a space's URL.
      parent='spaces/{space}',
        body=member).execute()

    # Prints details about the created membership.
    print(result)

if __name__ == '__main__':
    main()