from passlib.context import CryptContext  # type: ignore

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    # truncate password to 72 characters
    password = password[:72]
    return pwd_context.hash(password)

def veryfy_password(plain_password: str, hashed_password: str):
    # truncate password to 72 characters before verifying
    return pwd_context.verify(plain_password[:72], hashed_password)
