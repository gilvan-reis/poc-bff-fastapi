from datetime import datetime, timedelta
from typing import Optional

from fastapi import Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from grpc import StatusCode
from jose import jwt
from passlib.context import CryptContext


async def get_token_header(x_token: str = Header(...)):
    if x_token != 'secret-token':
        raise HTTPException(status_code=400, detail='X-Token header invalid')


async def get_query_token(token: str):
    if token != 'jessica':
        raise HTTPException(status_code=400, detail='No Jessica token provided')


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_payload(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_http_status_code_from_grpc_status(grpc_status: StatusCode):
    # list generated from https://grpc.github.io/grpc/python/grpc.html#grpc.StatusCode
    mapping_grpc_status_to_http_status_code = {
        StatusCode.OK: status.HTTP_200_OK,
        StatusCode.CANCELLED: status.HTTP_408_REQUEST_TIMEOUT,
        StatusCode.UNKNOWN: status.HTTP_500_INTERNAL_SERVER_ERROR,
        StatusCode.INVALID_ARGUMENT: status.HTTP_400_BAD_REQUEST,
        StatusCode.DEADLINE_EXCEEDED: status.HTTP_504_GATEWAY_TIMEOUT,
        StatusCode.NOT_FOUND: status.HTTP_404_NOT_FOUND,
        StatusCode.ALREADY_EXISTS: status.HTTP_409_CONFLICT,
        StatusCode.PERMISSION_DENIED: status.HTTP_403_FORBIDDEN,
        StatusCode.UNAUTHENTICATED: status.HTTP_401_UNAUTHORIZED,
        StatusCode.RESOURCE_EXHAUSTED: status.HTTP_429_TOO_MANY_REQUESTS,
        StatusCode.FAILED_PRECONDITION: status.HTTP_412_PRECONDITION_FAILED,
        StatusCode.ABORTED: status.HTTP_422_UNPROCESSABLE_ENTITY,
        StatusCode.UNIMPLEMENTED: status.HTTP_501_NOT_IMPLEMENTED,
        StatusCode.INTERNAL: status.HTTP_500_INTERNAL_SERVER_ERROR,
        StatusCode.UNAVAILABLE: status.HTTP_503_SERVICE_UNAVAILABLE,
        StatusCode.DATA_LOSS: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }

    return mapping_grpc_status_to_http_status_code.get(
        grpc_status, status.HTTP_500_INTERNAL_SERVER_ERROR)
