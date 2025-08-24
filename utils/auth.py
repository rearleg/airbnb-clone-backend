# utils/auth.py
import jwt
from datetime import datetime, timedelta
from django.conf import settings

def issue_app_jwt(user):
    now = datetime.utcnow()
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "iat": now,
        "exp": now + timedelta(minutes=settings.APP_JWT_EXP_MINUTES),
        "iss": "be-api",   # 식별용
    }
    return jwt.encode(payload, settings.APP_JWT_SECRET, algorithm=settings.APP_JWT_ALG)