from typing import Optional
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from pydantic import BaseModel

class Claims(BaseModel):
    uid: str
    email: str
    exp: Optional[int] = None
    iat: Optional[int] = None

security = HTTPBearer()

def parse_jwt_token(credentials: HTTPAuthorizationCredentials) -> Claims:
    """
    Parse JWT token from Authorization header and extract claims.
    
    Args:
        credentials: HTTPAuthorizationCredentials from FastAPI security
        
    Returns:
        Claims object containing uid and email
        
    Raises:
        HTTPException: If token is invalid or missing required claims
    """
    try:
        # Here you would typically verify the token with your secret key
        # For now, we'll just decode it without verification
        payload = jwt.decode(credentials.credentials, options={"verify_signature": False})
        
        if "uid" not in payload or "email" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing required claims"
            )
            
        return Claims(
            uid=payload["uid"],
            email=payload["email"],
            exp=payload.get("exp"),
            iat=payload.get("iat")
        )
        
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        ) 