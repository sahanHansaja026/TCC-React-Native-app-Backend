from fastapi import APIRouter, Depends, HTTPException, status  # type: ignore
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session  # type: ignore
from datetime import datetime, timedelta
from auth import hash_password, verify_password  # ✅ corrected import
import models, schemas
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

SECRET_KEY = "rvjlcZm0xTPUNEjhMIb8XhGIujqO_wuh7tQY5ShIuTs"
ALGORITHM = "HS256"

@router.post("/register/")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    
    new_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.password)  # uses Argon2
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.post("/login/")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    # ✅ Use verify_password from auth
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {"sub": db_user.email, "exp": expire}
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "message": "Login successful",
        "token": jwt_token,
        "username": db_user.username,
        "email": db_user.email
    }

@router.get("/me/")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": db_user.username,
        "email": db_user.email,
        "id": db_user.id,
    }
