from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_toke": form_data.username + "token"}


@app.get("/")
async def index(token: str = Depends(oauth2_scheme)):
    return {"the token": token}
