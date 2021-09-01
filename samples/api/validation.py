from google.auth.transport import requests
from google.oauth2 import id_token


# フロントからのリクエストを受け取り、headersのauthorizationからid_token（idToken）を受け取る。
# 受け取ったトークンを解析して、トークンが有効であるかを調べる。
def validate_token(function):
    def validate(root, info, **kwargs):
        print(kwargs)
        # Bearer token... の形式でトークンを受け取る。
        authorization = info.context.headers['authorization']
        # headersのauthorizationが空だった場合はエラー処理
        if authorization == '':
            raise ValueError('401 Unauthorized')
        token_type = authorization[:6]
        if token_type != 'Bearer':
            raise ValueError('not Bearer token!')
        token = authorization[7:]
        # print(token)
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            id_info = id_token.verify_oauth2_token(token, requests.Request())
            # print(id_info)
            # Or, if multiple clients access the backend server:
            # id_info = id_token.verify_oauth2_token(token, requests.Request())
            # if id_info['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If auth request is from a G Suite domain:
            # if id_info['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            # userid = id_info['sub']

            # キーワード引数にemailを追加
            kwargs['login_user_email'] = id_info['email']
            return function(root, info, **kwargs)
        except ValueError:
            raise ValueError('token is invalid')
    return validate
