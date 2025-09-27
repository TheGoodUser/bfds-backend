from datetime import datetime, timedelta
from jose import jwt # type: ignore

def CreateAccessToken(
    *,
    data: dict, 
    expires_delta: timedelta = None,
    secret_key:str, 
    algorithm: str, 
):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)
