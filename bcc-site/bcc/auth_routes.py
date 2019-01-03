from flask import Blueprint, redirect, url_for, request, session
import google.oauth2.credentials
from apiclient import discovery
import user
import google_auth_oauthlib.flow
auth_blueprint = Blueprint('auth', __name__)
from flask_login import login_user
scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/plus.me']

@auth_blueprint.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',
                                                                 scopes=scopes,
                                                                 redirect_uri=url_for('auth.oauth2callback',
                                                                                      _external=True))
    authorization_url, state = flow.authorization_url(
      access_type='offline',
      include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@auth_blueprint.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',
                scopes=scopes,
                redirect_uri=url_for('auth.oauth2callback', _external=True),
                state=state)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    session['credentials'] = credentials_to_dict(flow.credentials)
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    service = discovery.build('people', 'v1', credentials=credentials)
    session['email'] = service.people().get(resourceName='people/me', personFields='emailAddresses').execute()['emailAddresses'][0]['value']
    login_user(user.user(session['email']))
    return redirect("/")


@auth_blueprint.route('/clear')
def clear_credentials():
    if 'credentials' in session:
        del session['credentials']
    return redirect("/")


def credentials_to_dict(credentials):
    return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}
