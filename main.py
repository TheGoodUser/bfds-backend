from http.server import BaseHTTPRequestHandler
from fastapi import FastAPI, Request, Response, HTTPException, Depends, Cookie # type: ignore
from fastapi.responses import JSONResponse
from jose import JWTError, jwt #type: ignore
from datetime import datetime, timedelta
from starlette.middleware.base import BaseHTTPMiddleware

from models.user_model import UserModel
from monitoring.attacks.brute_force.brute_force_detector import BruteForceDetector

app = FastAPI()

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

app.add_middleware(DynamicCORS)

SECRET_KEY="Hello World"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60*24

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


# Create JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
 
     
# root
@app.get("/")
def welcome():
    return {'message': "Welcome User"}        

# IP
@app.get("/server-ip")
def server_ip():
    import socket
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return {"server_ip": ip}

# login
@app.post("/login")
async def login(response: Response, request: Request):
    
    # start the detector
    brute_force_detector.startDaemon(host_ip_add=request.client.host)
    
    # get the data
    data = await request.form()
    # convert to dict
    try:
        data = dict(data)
    except:
        raise Exception('Conversion Failed: Invalid request form format')
    
    # pass converted data to classmodel `UserModel`
    user_cred: UserModel = UserModel.from_json(data)


    # verify
    if user_cred.email != demo_user['email'] or user_cred.password != demo_user['password']:
        print("     [LOG]: Invalid credentials")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
    # generate the token
        token:str = create_access_token({"sub": user_cred.email}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True, # make it Fale while development
            samesite="none",
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
        samesite="none",
        secure=True # convert this to False in development
    )
    return {
        'message': "Logged out successfully",
        'ok': True,
        'status_code': 200
    }
    
    
# Dependency: Get current user from cookie
def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_cod=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=403, detail="Token verification failed")


# protected route
@app.get("/protected")
def protected_route(user: str = Depends(get_current_user)):
    return {
        'ok': True,
        'status_code': 200,
        "message": f"Welcome, {user}",
        "username": "Siddharth"
    }
        

