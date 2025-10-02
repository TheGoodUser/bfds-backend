from http.server import BaseHTTPRequestHandler
from fastapi import FastAPI, Request, Response, HTTPException, Depends, Cookie # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from jose import JWTError, jwt #type: ignore
from datetime import datetime, timedelta
from starlette.middleware.base import BaseHTTPMiddleware # type: ignore
from dotenv import load_dotenv # type: ignore

import os

from functions.jwt_generation import CreateAccessToken
from functions.get_current_user import CurrentUser

from models import UserModel
from monitoring.attacks.brute_force.brute_force_detector import BruteForceDetector

# load dotenv
load_dotenv()

# Determine if the environment is production
is_prod_env = os.getenv("IS_PRODUCTION", "False").lower()
is_prod: bool = True if is_prod_env in ("true", "1", "yes") else False

# Exception list
# All the blocked IP address are stored here
blocked_ips: list[str] = []

# Create a dynamic CORS to manage allow_origins=["*"] + credentials: "include"
class DynamicCORS(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        origin = request.headers.get("origin")
        
        # check for ip not being blocked
        ip = request.client.host
        if ip in blocked_ips:
            return JSONResponse(content={
                "message": "Forbidden: Your IP is blocked.",
                "ip": ip
            }, status_code=403)
        
        
        if origin:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "*"
            # if origin not in blocked_ips:
        return response

# App Instance
app = FastAPI()

app.add_middleware(DynamicCORS)

SECRET_KEY = "Hello World"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24


demo_user = {
    'email': 'ram19870101@gmail.com',
    'password': 'Test@123'
}


# Monitoring Instances
# Brute Force Detector
start_time: datetime = datetime.now()
brute_force_detector = BruteForceDetector(
    start_time = start_time, 
    blocked_ips = blocked_ips
)

# Current User Details
currentUser = CurrentUser(
    SECRET_KEY = SECRET_KEY, 
    ALOGORITHM = ALGORITHM
)


'''
All the API endpoints are defined form here on
'''

# root
@app.get("/")
def welcome(request: Request):
    try:
        is_cron_job = request.headers.get("amicronjob")
        if is_cron_job is not None:
            message = "      [CRON JOB CALL REQUESTED]"
            print(message)     
    except:
        pass
    return {'message': "Welcome User"}        


# login
@app.post("/login")
async def login(response: Response, request: Request):
    
    # start the auth monitoring
    brute_force_detector.start_daemon(host_ip_add = request.client.host)
    
    # get the data
    data = await request.form()
    # convert to dict
    try:
        data = dict(data)
    except:
        raise Exception('Conversion Failed: Invalid request form format')
    
    # pass converted data to classmodel `UserModel`
    userCred: UserModel = UserModel.from_json(data)

    # verify
    if userCred.email != demo_user['email'] or userCred.password != demo_user['password']:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        # generate the token
        token = CreateAccessToken(
            data = {"sub": userCred.email},
            expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            secret_key = SECRET_KEY,
            algorithm = ALGORITHM,
        )
        
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=is_prod,
            samesite="lax", # to allow cross-site requests
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
        return {
            'message': 'Login Successful',
            'ok': True,
            'status_code': 200
        }


# logout
@app.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        samesite="none", # to allow cross-site requests
        secure=is_prod # False while development
    )
    return {
        'message': "Logged out successfully",
        'ok': True,
        'status_code': 200
    }
  

# protected route
@app.get("/protected")
def protected_route(user: str = Depends(currentUser.get_details)):
    return {
        'ok': True,
        'status_code': 200,
        "message": f"Welcome, {user}",
        "username": "Siddharth"
    }
        

