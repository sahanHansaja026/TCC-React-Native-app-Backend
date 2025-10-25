from passlib.context import CryptContext  # type: ignore

# Use argon2 instead of bcrypt
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    """Hash a password with argon2"""
    return pwd_context.hash(password)

def veryfy_password(plain_password: str, hashed_password: str):
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)
