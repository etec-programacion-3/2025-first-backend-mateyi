from models import Libro, Usuario, IniciarSesion
from fastapi import FastAPI, HTTPException
import random

app=FastAPI()

libros_db = []
usuarios_db = []

### CREAR LIBRO
@app.post("/libros/{token}",response_model=Libro)
def crear_libro(nuevo_libro:Libro,token:int):
    for x in usuarios_db:
        if x.token == token:
            if x.rol == "admin":

                libros_db.append(nuevo_libro)
                return nuevo_libro
            
            raise HTTPException(status_code=403, detail="No tiene permisos para crear libros")
    raise HTTPException(status_code=401, detail="Token inválido")
###

### OBTENER TODOS LOS LIBROS
@app.get("/libros",response_model=list[Libro])
def obtener_libros():
    return libros_db
###

### OBTENER LIBRO POR ID
@app.get("/libros/{libro_id}",response_model=Libro)
def obtener_libro(libro_id: int):
    for x in libros_db:
        if x.id == libro_id:
            return x
        
    raise HTTPException(status_code=404, detail="Libro no encontrado")
###

### BORRAR LIBRO
@app.delete("/libros/{libro_id}/{token}")
def eliminar_libro(libro_id: int,token:int):
    for x in usuarios_db:
        if x.token == token:
            if x.rol == "admin":
                
                for x in libros_db:
                    if x.id == libro_id:
                        libros_db.remove(x)
                        return {"Mensaje" : "Libro eliminado"}
                return {"ERROR" : "Libro no encontrado"}
            
            raise HTTPException(status_code=403, detail="No tiene permisos para eliminar libros")
    raise HTTPException(status_code=401, detail="Token inválido")   
###

#####################################USUARIOS#####################################

###REGISTRAR USUARIO
@app.post("/usuarios",response_model=Usuario)
def registrar_usuario(nuevo_usuario:Usuario):
    usuarios_db.append(nuevo_usuario)
    return nuevo_usuario
###

### INICAR SESION
@app.post("/usuarios/login")
def iniciar_sesion(usuario:IniciarSesion):
    for x in usuarios_db:
        if x.id == usuario.id:
            if x.contrasena == usuario.contrasena:
                x.token = random.randint(100, 999)
                return {"Mensaje" : "Inicio de sesión exitoso. Su token es: " + str(x.token)}
            return {"ERROR" : "Contraseña incorrecta"}
        
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
###

### CERRAR SESION
@app.post("/usuarios/logout/{token}")
def cerrar_sesion(token:int):
    for x in usuarios_db:
        if x.token == token:
            x.token = None
            return {"Mensaje" : "Sesión cerrada exitosamente"}
    raise HTTPException(status_code=401, detail="Token inválido")
###

### OBTENER TODOS LOS USUARIOS
@app.get("/usuarios/{token}",response_model=list[Usuario| dict])
def obtener_usuarios(token :int):
    for x in usuarios_db:
        if x.token == token:
            if x.rol == "admin":
                return usuarios_db
            else:
                lista = []
                for y in usuarios_db:
                    lista.append({"id": y.id, "nombre": y.nombre, "rol": y.rol})
                return lista
    raise HTTPException(status_code=401, detail="Token inválido")
###

### OBTENER USUARIO POR ID
@app.get("/usuarios/{usuario_id}/{token}",response_model=Usuario | dict)
def obtener_usuario(usuario_id: int,token:int):
    for x in usuarios_db:
        if x.id == usuario_id:
            for y in usuarios_db:
                if y.token == token:
                    if y.rol == "admin":
                        return x
                    else:
                        return {"id": x.id, "nombre": x.nombre, "rol": x.rol}
                    
            raise HTTPException(status_code=401, detail="Token inválido")
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
###

