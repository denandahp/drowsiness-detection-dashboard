GOOGLE_CLIENT_ID = '668297879665-50jccldgf9i6ct1joti776k3qi4jpl2t.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
BASE_URI = 'http://127.0.0.1:8000'
SESSION_STATE = 'fpQNlpnBsf3Kjc4um6O189KmSsg1ll'

GOOGLE_REDIRECT_URI = f"{BASE_URI}/auth/login"
# GOOGLE_SCOPES = "https://www.googleapis.com/auth/drive"
GOOGLE_SCOPES = 'https://www.googleapis.com/auth/userinfo.email'
GOOGLE_LOGIN_REDIRECT_URI = ( f"https://accounts.google.com/o/oauth2/v2/auth?"
                              f"response_type=code"
                              f"&scope={GOOGLE_SCOPES}"
                              f"&access_type=offline"
                              f"&include_grant_scopes={'true'}"
                              f"&client_id={GOOGLE_CLIENT_ID}"
                              f"&redirect_uri={GOOGLE_REDIRECT_URI}")

'''
https://accounts.google.com/o/oauth2/v2/auth?
redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground
&prompt=consent
&response_type=code
&client_id=407408718192.apps.googleusercontent.com
&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive
&access_type=offline

https://accounts.google.com/o/oauth2/auth?
response_type=code
&client_id=668297879665-50jccldgf9i6ct1joti776k3qi4jpl2t.apps.googleusercontent.com
&redirect_uri=http%3A%2F%2Flocalhost%3A50469%2F
&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive
&state=qK1NTLtCbFDc8dUD6eUqbx7EeNFjQl
&access_type=offline
'''
