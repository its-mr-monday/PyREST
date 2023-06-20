import jwt
import datetime
from PyRest.Exceptions import PyRestSessionException, PyRestException

def is_expired(expiry: int) -> bool:
    expiry_t = datetime.datetime.fromtimestamp(expiry)
    now_t = datetime.datetime.now()
    if now_t > expiry_t:
        return True
    return False

def is_invalid(iat: int) -> bool:
    iat_t = datetime.datetime.fromtimestamp(iat)
    now_t = datetime.datetime.now()
    if now_t < iat_t:
        return False
    return True
    

def decrypt_jwt(val: str, key: str) -> dict:
    try:
        return jwt.decode(val, key, algorithms=["HS256"])
    except Exception as e:
        raise PyRestException(e)
    
class RefreshToken:
    def __init__(self, username: str, user_id: int, expiry: int, iat: int):
        self.user = username
        self.uid = user_id
        self.exp = expiry
        self.iat = iat
        self.token = {
            "user": username,
            "uid": user_id,
            "exp": expiry,
            "iat": iat,
            "type": "refresh"
        }
        
    def is_expired(self) -> bool:
        return is_expired(self.exp)

    def export_token(self, secret_key: str) -> str | None:
        if self.is_expired():
            raise PyRestSessionException("Session has expired")
        if is_invalid(self.iat):
            raise PyRestSessionException("Session is invalid")
        try:
            exported = jwt.encode(self.token, secret_key, algorithm="HS256")
            return exported
        except Exception as e:
            raise PyRestException(e)

class SessionToken:
    def __init__(self, username: str, user_id: int, expiry: int, iat: int):
        self.user = username
        self.uid = user_id
        self.exp = expiry
        self.iat = iat
        self.token = {
            "user": username,
            "uid": user_id,
            "exp": expiry,
            "iat": iat,
            "type": "session"
        }
        
    def is_expired(self) -> bool:
        return is_expired(self.exp)

    def export_token(self, secret_key: str) -> str | None:
        if self.is_expired():
            raise PyRestSessionException("Session has expired")
        if is_invalid(self.iat):
            raise PyRestSessionException("Session is invalid")
        try:
            exported = jwt.encode(self.token, secret_key, algorithm="HS256")
            return exported
        except Exception as e:
            raise PyRestException(e)
        
    
        

class SessionManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.session_cache = self.__load_refresh_cache__()
        self.refresh_cache = self.__load_refresh_cache__()
    
    def __load_session_cache__(self) -> dict[str, SessionToken]:
        #Loads the session cache from the database
        return {}
    
    def __load_refresh_cache__(self) -> dict[str, RefreshToken]:
        #Loads the refresh cache from the database
        return {}
    
    def decode_session_token(self, token: str) -> SessionToken:
        if token in self.session_cache:
            sessionToken = self.session_cache[token]
            if sessionToken.is_expired():
                self.session_cache.pop(token)
                raise PyRestSessionException("Session has expired")
            return sessionToken
        try:
            tk = decrypt_jwt(token, self.secret_key)
            if "type" not in tk or tk["type"] != "session":
                raise PyRestSessionException("Invalid session token")
            obj = SessionToken(tk["user"], tk["uid"], tk["exp"], tk["iat"])
            if not obj.is_expired():
                self.session_cache[token] = obj
                return obj
        except Exception as e:
            raise PyRestException(e)
        raise PyRestSessionException("Invalid session token")
        
    def decode_refresh_token(self, token: str) -> RefreshToken:
        if token in self.refresh_cache:
            #Check if the token is expired
            refreshToken = self.refresh_cache[token]
            if refreshToken.is_expired():
                self.refresh_cache.pop(token)
                raise PyRestSessionException("Refresh token has expired")
            return refreshToken
        try:
            tk = decrypt_jwt(token, self.secret_key)
            if "type" not in tk or tk["type"] != "refresh":
                raise PyRestSessionException("Invalid refresh token")
            obj = RefreshToken(tk["user"], tk["uid"], tk["exp"], tk["iat"])
            if not obj.is_expired():
                self.session_cache[token] = obj
                return obj
        except Exception as e:
            raise PyRestException(e)
        raise PyRestSessionException("Invalid refresh token")
            

    def login_tokens(self, username: str, user_id: int) -> tuple(SessionToken, RefreshToken):
        #Creates the login tokens
        now = int(datetime.datetime.now().timestamp())
        s_exp = now + 3600
        r_exp = now + 86400
        stk = SessionToken(username, user_id, s_exp, now)
        rtk = RefreshToken(username, user_id, r_exp, now)
        return (stk, rtk)
    
        