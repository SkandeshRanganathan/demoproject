from jose import JWTError ,jwt
from datetime import datetime , timedelta

from app import schemas


SECRET_KEY ="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_toke(data : dict):
    to_en = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_en.update({"exp" : expire})

    encoded = jwt.encode(to_en , SECRET_KEY , algorithm=ALGORITHM )

    return encoded

def verify_at(token : str , credentials_excecption):
    try : 
        payload = jwt.decode(token , SECRET_KEY, algorithms=ALGORITHM )
        id : str = payload.get("users_id")

        if id is None:
            raise credentials_excecption
        
        token_data = schemas.TokenData(id = id)
    except JWTError : 
        raise credentials_excecption
    
