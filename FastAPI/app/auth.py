from datetime import (  # used to handle expiry time for tokens
    datetime,
    timedelta,
)

import jwt  # used for encoding and decoding jwt tokens

from fastapi import HTTPException  # used to handle error handling


class Auth:
    secret = "jjj"

    def encode_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)

    def encode_token(self, username):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=30),
            "iat": datetime.utcnow(),
            "scope": "access_token",
            "sub": username,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "access_token":
                return payload["sub"]
            raise HTTPException(
                status_code=401, detail="Scope for the token is invalid"
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
