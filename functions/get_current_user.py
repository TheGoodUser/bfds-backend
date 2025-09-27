from fastapi import HTTPException, Cookie # type: ignore
from jose import jwt, JWTError # type: ignore

class CurrentUser():
    def __init__(self, SECRET_KEY: str, ALOGORITHM: str):
        self.SECRET_KEY = SECRET_KEY
        self.ALOGORITHM = ALOGORITHM
        
    # Dependency: Get current user from cookie
    def get_details(self, *, access_token: str = Cookie(None)) -> str:
        if not access_token:
            raise HTTPException(status_code=401, detail="Not Authenticated")
        try:
            payload = jwt.decode(access_token, self.SECRET_KEY, algorithms=[self.ALOGORITHM])
            email = payload.get("sub")
            if email is None:
                raise HTTPException(status_cod=401, detail="Invalid token")
            return email
        except JWTError:
            raise HTTPException(status_code=403, detail="Token verification failed")
