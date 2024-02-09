import sys
sys.path.append("..")

from fastapi import Depends, HTTPException, status, APIRouter, Request
from pydantic import BaseModel
from typing import Optional
import model
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from HRdatabase import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.exc import IntegrityError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



SECRET_KEY = "Yams-farm19"
ALGORITHM = "HS256"

templates = Jinja2Templates(directory="templates")

class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

model.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, db):
    user = db.query(model.Users)\
         .filter(model.Users.username == username)\
         .first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        paylaod = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = paylaod.get("sub")
        user_id: int = paylaod.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()

@router.get("/", response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse("Login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})




@router.post("/create/user")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    try:
        create_user_model = model.Users(**create_user.dict())
        create_user_model.hashed_password = get_password_hash(create_user.password)
        create_user_model.is_active = True
        db.add(create_user_model)
        db.commit()
        db.refresh(create_user_model)  # Refresh the model to get the auto-generated fields
        return create_user_model
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    return {"token": token}




def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception

def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response
