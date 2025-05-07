from pydantic import BaseModel

class Libro(BaseModel):
    id: int
    titulo: str
    autor: str
    anio: int
    genero: str

class Usuario(BaseModel):
    id: int
    nombre: str
    contrasena: str
    rol: str
    token: int = None

class IniciarSesion(BaseModel):
    id: int
    contrasena: str