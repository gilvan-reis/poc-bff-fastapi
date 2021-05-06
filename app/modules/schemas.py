from pydantic import BaseModel


class ClearCacheParams(BaseModel):
    namespace: str


class Token(BaseModel):
    access_token: str
    token_type: str
