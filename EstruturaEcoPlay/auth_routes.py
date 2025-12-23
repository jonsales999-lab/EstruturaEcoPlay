from fastapi import APIRouter, Depends, HTTPException, status
from schemas import UsuarioCreate, LoginSchema
from main import bcrypt_context,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,SECRET_KEY
from jose import jwt, JWTError#gerador de token
from models import Usuario
from sqlalchemy.orm import Session
from dependencies import pegar_sesssao,verificar_token
from datetime import datetime, timedelta,timezone
from fastapi.security import OAuth2PasswordRequestForm
auth_router = APIRouter(prefix="/auth", tags=["auth"])
import base64#Base 64 
#Cricao do tokent jwt
def criar_token(id_usuario, duracao_token = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)):

    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado



#Verificacao de USUARIO
def autenticar_usuario(email,senha,session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not usuario.senha_hash or not bcrypt_context.verify(senha, usuario.senha_hash):
        return False
    return usuario


@auth_router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_usuario(user: UsuarioCreate, session = Depends(pegar_sesssao)):
    
    usuario = session.query(Usuario).filter(Usuario.email == user.email).first()
    if usuario:
        #VERIFICA se o USUARIO já está CADASTRADO
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail = "Email já cadastrado")
    
    # Função interna simples para tratar o Base64
    def converter_base64_para_binario(string_b64: str):
        if not string_b64:
            return None
        try:
            # Se o front enviar com o prefixo "data:image/jpeg;base64,", nós removemos
            if "," in string_b64:
                string_b64 = string_b64.split(",")[1]
            return base64.b64decode(string_b64)
        except Exception:
            raise HTTPException(status_code=400, detail="Formato de imagem inválido")
    
    
    
    senha_hash = bcrypt_context.hash(user.senha)
    # Cria o usuário
    novo_usuario = Usuario(
        nome_completo=user.nome_completo,
        sexo=user.sexo,
        data_nascimento=user.data_nascimento,
        funcao=user.funcao,
        telefone_pessoal=user.telefone_pessoal,
        email=user.email,
        rg_path=converter_base64_para_binario(user.rg_path),
        cpf_path=converter_base64_para_binario(user.cpf_path),
        senha_hash=senha_hash,
        cursando=user.cursando,
        manequim=user.manequim,
        tipo_sanguineo=user.tipo_sanguineo,
        medicamento_controlado=user.medicamento_controlado,
        nome_medicamento_1=user.nome_medicamento_1,
        declaracao_lida=user.declaracao_lida,
    )

    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)
    return {"mensagem": "Usuário cadastrado com sucesso", "id": novo_usuario.id}


@auth_router.post("/login")
async def login(login : LoginSchema, session = Depends(pegar_sesssao)):
    usuario = autenticar_usuario(login.email, login.senha, session)  # lembrar de validar com a senha
    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail = "Usuario não encontrado credenciais invalidas")
    
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token = timedelta(days=7))
        return{
            "access_token" : access_token,
            "refresh_token" : refresh_token,
            "token_type":"Bearer"
            
            }
#
@auth_router.post("/login-form")
async def login_form(dados_formulario : OAuth2PasswordRequestForm = Depends(), session : Session = Depends(pegar_sesssao)):
    usuario = autenticar_usuario(dados_formulario.username,dados_formulario.password,session)  # lembrar de validar com a senha
    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail = "Usuario não encontrado credenciais invalidas")
    
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token = timedelta(days=7))
        return{
            "access_token" : access_token,
            "refresh_token" : refresh_token,
            "token_type":"Bearer"
            
            }


@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return{
        "access_token" : access_token,
        "token_type" : "Bearer"
    }
