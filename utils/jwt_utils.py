from typing import Optional
from fastapi import HTTPException, status, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from pydantic import BaseModel
from loguru import logger

class Claims(BaseModel):
    uid: str  # This is the user_id as per the requirements
    email: Optional[str] = None
    exp: Optional[int] = None
    iat: Optional[int] = None

security = HTTPBearer()

def parse_jwt_token(credentials: HTTPAuthorizationCredentials) -> Claims:
    """
    Parse JWT token from Authorization header and extract claims.
    
    Args:
        credentials: HTTPAuthorizationCredentials from FastAPI security
        
    Returns:
        Claims object containing uid (user_id) and other claims
        
    Raises:
        HTTPException: If token is invalid or missing required claims
    """
    try:
        # Here you would typically verify the token with your secret key
        # For now, we'll just decode it without verification
        payload = jwt.decode(credentials.credentials, options={"verify_signature": False})
        
        if "uid" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing uid claim"
            )
            
        return Claims(
            uid=payload["uid"],  # This uid is the user_id
            email=payload.get("email"),
            exp=payload.get("exp"),
            iat=payload.get("iat")
        )
        
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Convenience function to get just the user_id from the JWT token.
    
    Args:
        credentials: HTTPAuthorizationCredentials from FastAPI security
        
    Returns:
        user_id extracted from the JWT token
    """
    claims = parse_jwt_token(credentials)
    return claims.uid  # Return the uid as user_id 