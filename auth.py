from passlib.context import CryptContext

# Use Argon2 instead of bcrypt
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    """Hash the password using Argon2"""
    return pwd_context.hash(password)

def veryfy_password(plain_password: str, hash_password: str):
    """Verify the password using Argon2"""
    return pwd_context.verify(plain_password, hash_password)
