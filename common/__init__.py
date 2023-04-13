from .error_handling import add_custom_errors
from .cors_handling import handle_cors
from .response_messages import ResponseMessagesValues
from .middlewares_handling import decryptor_middleware

import fastapi.security

oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl="session/login")
token_schema = fastapi.security.HTTPBearer()
