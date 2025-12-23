from fastapi import Depends,HTTPException
from main import SECRET_KEY, ALGORITHM,oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker,Session
from models import Usuario
from jose import jwt, JWTError

def pegar_sesssao():
    try:
        # `db` is an Engine instance returned by create_engine
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

#Verifica se o token do usuario e valido para liberar o login
def verificar_token(token: str = Depends(oauth2_schema), session : Session = Depends(pegar_sesssao)):
    try:
        dic_info = jwt.decode(token,SECRET_KEY,ALGORITHM)
        id_usuario = int(dic_info.get("sub"))#Pega o id do usuario da funcao de criacao de token e converte para dicionario pois o jwt e recebido nesse formato
    except JWTError:
        
        
        raise HTTPException(status_code=401, detail = "Acesso Negado, verifique a validade do token")
    
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail = "Acesso Invalido")
    return usuario