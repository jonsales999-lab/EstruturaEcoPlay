from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
import base64


class UsuarioCreate(BaseModel):
    nome_completo: Optional[str] = None
    sexo: Optional[str] = None
    data_nascimento: Optional[date] = None
    funcao: Optional[str] = None
    telefone_pessoal: Optional[str] = None
    rg_path: Optional[str] = None
    cpf_path: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: str = None
    cursando: Optional[str] = None
    manequim: Optional[str] = None
    tipo_sanguineo: Optional[str] = None
    medicamento_controlado: Optional[bool] = None
    nome_medicamento_1: Optional[str] = None
    declaracao_lida: Optional[bool] = None
    
    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: Optional[str] = None
    senha: Optional[str] = None