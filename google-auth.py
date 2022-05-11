from fastapi import FastAPI, Request
import os
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth,  OAuthError
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()

# Authentication

# OAuth settings
GOOGLE_CLIENT_ID = "863179219367-nma6o3317b8tkn0jb7lrrhuki5n4bbmc.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "22ep7GPJbTigGatmm6cyouQc"


# Set up oauth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID,
               'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

app.add_middleware(SessionMiddleware, secret_key="secret-string")


# Authentication


@app.get('/')
def index(request: Request):
    user = request.session.get('email')
    if user:
        name = user.get('name')
        return HTMLResponse(f'<p>Hello {name}!</p><a href=/logout>Logout</a>')
    return HTMLResponse('<a href=/login>Login</a>')


@app.route('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route('/auth')
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get("userinfo")
    if user:
        request.session["user"] = dict(user)
    return RedirectResponse(url="/")


@app.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')
